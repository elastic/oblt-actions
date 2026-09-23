const fs = require("fs");
const path = require("path");
const os = require("os");
const simpleGit = require("simple-git");
const {
  enqueue,
  waitForSlot,
  dequeue,
  createRequesterId,
  parseRunIdFromRequesterId,
  pruneDeadRuns,
} = require("./utils");

describe("Queue Unit & Integration Tests", () => {
  test("createRequesterId and parseRunIdFromRequesterId formatting", () => {
    process.env.GITHUB_RUN_ID = "987654";
    process.env.GITHUB_RUN_ATTEMPT = "2";

    const id = createRequesterId("worker-1");
    expect(id).toMatch(/^987654:2:worker-1:\d+-\d+$/);

    const parsedRunId = parseRunIdFromRequesterId(id);
    expect(parsedRunId).toBe("987654");
  });

  describe("Queue concurrency and slot management", () => {
    let bareRepo;
    let ws1, ws2, ws3;

    async function createBareRepo() {
      const repoDir = fs.mkdtempSync(path.join(os.tmpdir(), "queue-bare-"));
      const git = simpleGit(repoDir);
      await git.init(["--bare"]);
      return repoDir;
    }

    async function createWorkspace(bareRepoPath, name) {
      const wsDir = fs.mkdtempSync(path.join(os.tmpdir(), `queue-ws-${name}-`));
      const git = simpleGit(wsDir);
      await git.init();
      await git.addConfig("user.name", "Test User");
      await git.addConfig("user.email", "test@example.com");

      const queuePath = path.join(wsDir, "job_queue");
      fs.writeFileSync(queuePath, "");
      await git.add("job_queue");
      await git.commit("init");

      await git.addRemote("origin", bareRepoPath);
      await git.checkout(["-b", "job-queue"]);
      await git.push(["--set-upstream", "origin", "job-queue"]);
      return wsDir;
    }

    async function createWorkspaceClone(bareRepoPath, name) {
      const wsDir = fs.mkdtempSync(path.join(os.tmpdir(), `queue-ws-${name}-`));
      const git = simpleGit(wsDir);
      await git.init();
      await git.addConfig("user.name", "Test User");
      await git.addConfig("user.email", "test@example.com");
      await git.addRemote("origin", bareRepoPath);
      await git.fetch(["origin", "job-queue", "-q"]);
      await git.checkout(["--track", "origin/job-queue"]);
      return wsDir;
    }

    beforeAll(async () => {
      bareRepo = await createBareRepo();
      ws1 = await createWorkspace(bareRepo, "job1");
      ws2 = await createWorkspaceClone(bareRepo, "job2");
      ws3 = await createWorkspaceClone(bareRepo, "job3");
    });

    afterAll(() => {
      try {
        fs.rmSync(bareRepo, { recursive: true, force: true });
        if (ws1) fs.rmSync(ws1, { recursive: true, force: true });
        if (ws2) fs.rmSync(ws2, { recursive: true, force: true });
        if (ws3) fs.rmSync(ws3, { recursive: true, force: true });
      } catch (e) {}
    });

    test("allows up to concurrency limit (N=2) to acquire slot immediately while 3rd waits", async () => {
      const branch = "job-queue";
      const queueFile = "job_queue";

      const job1Id = "101:1:worker-1:1";
      const job2Id = "102:1:worker-2:2";
      const job3Id = "103:1:worker-3:3";

      // Job 1 and 2 enqueue
      await enqueue(branch, queueFile, job1Id, ws1, 1, 2, 2, false);
      await enqueue(branch, queueFile, job2Id, ws2, 1, 2, 2, false);

      // Both job 1 and 2 acquire slot because concurrencyLimit = 2
      await waitForSlot(branch, queueFile, job1Id, ws1, 1, 2, false);
      await waitForSlot(branch, queueFile, job2Id, ws2, 1, 2, false);

      // Job 3 enqueues
      await enqueue(branch, queueFile, job3Id, ws3, 1, 2, 2, false);

      // Verify queue has all 3
      const git1 = simpleGit(ws1);
      await git1.fetch(["origin", branch, "-q"]);
      await git1.reset(["--hard", `origin/${branch}`, "-q"]);
      let queue = fs
        .readFileSync(path.join(ws1, queueFile), "utf8")
        .trim()
        .split("\n")
        .filter(Boolean);
      expect(queue).toEqual([job1Id, job2Id, job3Id]);

      // Job 1 finishes and releases slot
      await dequeue(branch, queueFile, job1Id, ws1, 1);

      // Now job 3 should be able to acquire slot (position is now index 1 < 2)
      await waitForSlot(branch, queueFile, job3Id, ws3, 1, 2, false);

      // Release remaining jobs
      await dequeue(branch, queueFile, job2Id, ws2, 1);
      await dequeue(branch, queueFile, job3Id, ws3, 1);

      await git1.fetch(["origin", branch, "-q"]);
      await git1.reset(["--hard", `origin/${branch}`, "-q"]);
      const finalQueue = fs
        .readFileSync(path.join(ws1, queueFile), "utf8")
        .trim()
        .split("\n")
        .filter(Boolean);
      expect(finalQueue).toEqual([]);
    }, 30000);
  });
});
