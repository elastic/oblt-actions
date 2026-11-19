const fs = require("fs");
const os = require("os");
const path = require("path");

jest.mock("@actions/core", () => ({
  info: jest.fn(),
  error: jest.fn(),
  debug: jest.fn(),
  warning: jest.fn(),
}));

jest.mock("simple-git", () => jest.fn());

const core = require("@actions/core");
const simpleGit = require("simple-git");
const { setUpRepo, syncBranch, enqueue, dequeue } = require("./utils");

function createGitMock() {
  return {
    init: jest.fn().mockResolvedValue(undefined),
    addConfig: jest.fn().mockResolvedValue(undefined),
    removeRemote: jest.fn().mockResolvedValue(undefined),
    addRemote: jest.fn().mockResolvedValue(undefined),
    checkout: jest.fn().mockResolvedValue(undefined),
    branch: jest.fn().mockResolvedValue(undefined),
    fetch: jest.fn().mockResolvedValue(undefined),
    reset: jest.fn().mockResolvedValue(undefined),
    clean: jest.fn().mockResolvedValue(undefined),
    add: jest.fn().mockResolvedValue(undefined),
    commit: jest.fn().mockResolvedValue(undefined),
    push: jest.fn().mockResolvedValue(undefined),
  };
}

function createTempDir() {
  return fs.mkdtempSync(path.join(os.tmpdir(), "mutex-test-"));
}

describe("utils", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test("setUpRepo initializes git config and adds origin", async () => {
    const git = createGitMock();
    git.removeRemote.mockRejectedValueOnce(new Error("not found"));
    simpleGit.mockReturnValue(git);

    await setUpRepo("https://example/repo", "/tmp/repo");

    expect(simpleGit).toHaveBeenCalledWith("/tmp/repo");
    expect(git.init).toHaveBeenCalledTimes(1);
    expect(git.addConfig).toHaveBeenNthCalledWith(1, "user.name", "github-bot");
    expect(git.addConfig).toHaveBeenNthCalledWith(
      2,
      "user.email",
      "github-bot@users.noreply.github.com"
    );
    expect(git.addRemote).toHaveBeenCalledWith("origin", "https://example/repo");
  });

  test("syncBranch syncs tracking branch then creates orphan if tracking fails", async () => {
    const git = createGitMock();
    // First checkout (tracking) fails, second checkout (orphan) succeeds
    git.checkout
      .mockRejectedValueOnce(new Error("branch not found"))
      .mockResolvedValueOnce(undefined);

    const deadline = { endTime: Date.now() + 60000, startTime: Date.now(), timeoutMinutes: 1 };
    await syncBranch("mutex", git, deadline, "test-job");

    // Should attempt reset/clean
    expect(git.reset).toHaveBeenCalledWith(["--hard", "--quiet"]);
    expect(git.clean).toHaveBeenCalledWith(["--force", "-d", "--quiet"]);
    // Should delete local branch
    expect(git.branch).toHaveBeenCalledWith(["-D", "mutex", "-q"]);
    // Should fetch from remote
    expect(git.fetch).toHaveBeenCalledWith(["origin", "mutex", "-q"]);
    // Should try tracking branch first (fails)
    expect(git.checkout).toHaveBeenNthCalledWith(1, ["-B", "mutex", "origin/mutex", "-q"]);
    // Should fall back to orphan when tracking fails
    expect(git.checkout).toHaveBeenNthCalledWith(2, ["-q", "--orphan", "mutex"]);
  });

  test("syncBranch successfully checks out tracking branch", async () => {
    const git = createGitMock();
    const deadline = { endTime: Date.now() + 60000, startTime: Date.now(), timeoutMinutes: 1 };
    await syncBranch("mutex", git, deadline, "test-job");

    // Should attempt reset/clean
    expect(git.reset).toHaveBeenCalledWith(["--hard", "--quiet"]);
    expect(git.clean).toHaveBeenCalledWith(["--force", "-d", "--quiet"]);
    // Should delete local branch
    expect(git.branch).toHaveBeenCalledWith(["-D", "mutex", "-q"]);
    // Should fetch from remote
    expect(git.fetch).toHaveBeenCalledWith(["origin", "mutex", "-q"]);
    // Should checkout tracking branch (only checkout call)
    expect(git.checkout).toHaveBeenNthCalledWith(1, ["-B", "mutex", "origin/mutex", "-q"]);
  });

  test("enqueue appends request and pushes commit", async () => {
    const git = createGitMock();
    simpleGit.mockReturnValue(git);
    const cwd = createTempDir();

    try {
      await enqueue("mutex", "mutex_queue", "requester-1", cwd, 30);

      const queueContent = fs.readFileSync(path.join(cwd, "mutex_queue"), "utf8");
      expect(queueContent).toBe("requester-1\n");
      expect(git.add).toHaveBeenCalledWith("mutex_queue");
      expect(git.commit).toHaveBeenCalledWith("[requester-1] Enqueue", ["-q"]);
      expect(git.push).toHaveBeenCalledWith(["--set-upstream", "origin", "mutex", "-q"]);
    } finally {
      fs.rmSync(cwd, { recursive: true, force: true });
    }
  });

  test("enqueue does not append duplicate request", async () => {
    const git = createGitMock();
    simpleGit.mockReturnValue(git);
    const cwd = createTempDir();

    try {
      fs.writeFileSync(path.join(cwd, "mutex_queue"), "requester-1\n");

      await enqueue("mutex", "mutex_queue", "requester-1", cwd, 30);

      expect(git.add).not.toHaveBeenCalled();
      expect(git.commit).not.toHaveBeenCalled();
      expect(git.push).not.toHaveBeenCalled();
    } finally {
      fs.rmSync(cwd, { recursive: true, force: true });
    }
  });

  test("dequeue removes head request and commits unlock", async () => {
    const git = createGitMock();
    simpleGit.mockReturnValue(git);
    const cwd = createTempDir();

    try {
      fs.writeFileSync(path.join(cwd, "mutex_queue"), "requester-1\nrequester-2\n");

      await dequeue("mutex", "mutex_queue", "requester-1", cwd, 30);

      const queueContent = fs.readFileSync(path.join(cwd, "mutex_queue"), "utf8");
      expect(queueContent).toBe("requester-2\n");
      expect(git.commit).toHaveBeenCalledWith("[requester-1] Unlock", ["-q"]);
      expect(git.push).toHaveBeenCalledWith(["--set-upstream", "origin", "mutex", "-q"]);
    } finally {
      fs.rmSync(cwd, { recursive: true, force: true });
    }
  });

  test("enqueue throws timeout error when deadline exceeded", async () => {
    const git = createGitMock();
    git.push.mockRejectedValue(new Error("push failed"));
    simpleGit.mockReturnValue(git);
    const cwd = createTempDir();

    try {
      // Use 0 timeout (immediately expired)
      await expect(enqueue("mutex", "mutex_queue", "requester-1", cwd, 0)).rejects.toThrow(
        expect.objectContaining({
          message: expect.stringMatching(/Enqueue.*timed out/),
        })
      );
    } finally {
      fs.rmSync(cwd, { recursive: true, force: true });
    }
  });

  test("enqueue timeout error includes requester ID", async () => {
    const git = createGitMock();
    git.push.mockRejectedValue(new Error("push failed"));
    simpleGit.mockReturnValue(git);
    const cwd = createTempDir();

    try {
      // Use 0 timeout (immediately expired)
      await expect(enqueue("mutex", "mutex_queue", "requester-123", cwd, 0)).rejects.toThrow(
        expect.objectContaining({
          message: expect.stringMatching(/\[requester-123\]/),
        })
      );
    } finally {
      fs.rmSync(cwd, { recursive: true, force: true });
    }
  });

  test("dequeue throws timeout error when deadline exceeded", async () => {
    const git = createGitMock();
    simpleGit.mockReturnValue(git);
    const cwd = createTempDir();

    try {
      fs.writeFileSync(path.join(cwd, "mutex_queue"), "requester-1\n");

      // Use 0 timeout (immediately expired)
      await expect(
        dequeue("mutex", "mutex_queue", "requester-1", cwd, 0)
      ).rejects.toThrow(
        expect.objectContaining({
          message: expect.stringMatching(/\[requester-1\].*Dequeue.*timed out/),
        })
      );
    } finally {
      fs.rmSync(cwd, { recursive: true, force: true });
    }
  });
});
