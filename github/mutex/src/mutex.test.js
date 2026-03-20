const fs = require("fs");
const path = require("path");
const os = require("os");
const simpleGit = require("simple-git");
const { enqueue, dequeue } = require("./utils");

// Helper to create a bare git repo for shared state
async function createBareRepo() {
  const repoDir = fs.mkdtempSync(path.join(os.tmpdir(), "mutex-bare-"));
  const git = simpleGit(repoDir);
  await git.init(["--bare"]);
  return repoDir;
}

// Helper to create a workspace that clones from the bare repo
async function createWorkspace(bareRepoPath, name) {
  const wsDir = fs.mkdtempSync(path.join(os.tmpdir(), `mutex-ws-${name}-`));
  const git = simpleGit(wsDir);

  // Initialize a local repo first
  await git.init();
  await git.addConfig("user.name", "Test User");
  await git.addConfig("user.email", "test@example.com");

  // Create an initial commit
  const queuePath = path.join(wsDir, "mutex_queue");
  fs.writeFileSync(queuePath, "");
  await git.add("mutex_queue");
  await git.commit("init");

  // Add the bare repo as remote and push
  await git.addRemote("origin", bareRepoPath);
  await git.checkout(["-b", "mutex"]);
  await git.push(["--set-upstream", "origin", "mutex"]);

  return wsDir;
}

// Helper to create a workspace that shares an existing mutex branch
async function createWorkspaceClone(bareRepoPath, name) {
  const wsDir = fs.mkdtempSync(path.join(os.tmpdir(), `mutex-ws-${name}-`));
  const git = simpleGit(wsDir);

  // Initialize a local repo first
  await git.init();
  await git.addConfig("user.name", "Test User");
  await git.addConfig("user.email", "test@example.com");

  // Add the bare repo as remote
  await git.addRemote("origin", bareRepoPath);

  // Fetch the existing mutex branch
  await git.fetch(["origin", "mutex", "-q"]);
  await git.checkout(["--track", "origin/mutex"]);

  return wsDir;
}

describe("Mutex Integration - Enqueue/Dequeue with 3 jobs", () => {
  let bareRepo;
  let job1Ws, job2Ws, job3Ws;

  beforeAll(async () => {
    bareRepo = await createBareRepo();

    // Only job1 initializes the shared mutex branch
    job1Ws = await createWorkspace(bareRepo, "job1");

    // Jobs 2 and 3 clone from the same bare repo (which now has the mutex branch from job1)
    job2Ws = await createWorkspaceClone(bareRepo, "job2");
    job3Ws = await createWorkspaceClone(bareRepo, "job3");
  });

  afterAll(() => {
    try {
      fs.rmSync(bareRepo, { recursive: true, force: true });
      if (job1Ws) fs.rmSync(job1Ws, { recursive: true, force: true });
      if (job2Ws) fs.rmSync(job2Ws, { recursive: true, force: true });
      if (job3Ws) fs.rmSync(job3Ws, { recursive: true, force: true });
    } catch (e) {
      // Ignore cleanup errors
    }
  });

  test(
    "enqueue 3 jobs and dequeue them sequentially",
    async () => {
      const queueFile = "mutex_queue";
      const branch = "mutex";

      // All 3 jobs enqueue themselves (using longer timeout to allow retries)
      await enqueue(branch, queueFile, "job-1", job1Ws, 1);  // 60 seconds
      console.log("Job 1 enqueued");
      await simpleGit(job1Ws).fetch(["origin", branch, "-q"]);
      let queue = fs
        .readFileSync(path.join(job1Ws, queueFile), "utf8")
        .trim()
        .split("\n")
        .filter(Boolean);
      console.log("Queue after job-1:", queue);

      await enqueue(branch, queueFile, "job-2", job2Ws, 1);  // 60 seconds
      console.log("Job 2 enqueued");
      await simpleGit(job2Ws).fetch(["origin", branch, "-q"]);
      queue = fs
        .readFileSync(path.join(job2Ws, queueFile), "utf8")
        .trim()
        .split("\n")
        .filter(Boolean);
      console.log("Queue after job-2:", queue);

      await enqueue(branch, queueFile, "job-3", job3Ws, 1);  // 60 seconds
      console.log("Job 3 enqueued");
      await simpleGit(job3Ws).fetch(["origin", branch, "-q"]);
      queue = fs
        .readFileSync(path.join(job3Ws, queueFile), "utf8")
        .trim()
        .split("\n")
        .filter(Boolean);
      console.log("Queue after job-3:", queue);

    // Verify queue from job1's perspective after fetch
    const git1 = simpleGit(job1Ws);
    await git1.fetch(["origin", branch, "-q"]);
    let queue = fs
      .readFileSync(path.join(job1Ws, queueFile), "utf8")
      .trim()
      .split("\n")
      .filter(Boolean);
    expect(queue).toEqual(["job-1", "job-2", "job-3"]);

    // Job 1 dequeues (has lock at position 0)
    await dequeue(branch, queueFile, "job-1", job1Ws, 5);

    // Verify job-1 is gone
    await git1.fetch(["origin", branch, "-q"]);
    queue = fs
      .readFileSync(path.join(job1Ws, queueFile), "utf8")
      .trim()
      .split("\n")
      .filter(Boolean);
    expect(queue).toEqual(["job-2", "job-3"]);

    // Job 2 dequeues (has lock at position 0)
    const git2 = simpleGit(job2Ws);
    await git2.fetch(["origin", branch, "-q"]);
    await dequeue(branch, queueFile, "job-2", job2Ws, 5);

    // Verify job-2 is gone
    await git2.fetch(["origin", branch, "-q"]);
    queue = fs
      .readFileSync(path.join(job2Ws, queueFile), "utf8")
      .trim()
      .split("\n")
      .filter(Boolean);
    expect(queue).toEqual(["job-3"]);

    // Job 3 dequeues (has lock at position 0)
    const git3 = simpleGit(job3Ws);
    await git3.fetch(["origin", branch, "-q"]);
    await dequeue(branch, queueFile, "job-3", job3Ws, 5);

    // Verify queue is empty
    await git3.fetch(["origin", branch, "-q"]);
    const content = fs.readFileSync(path.join(job3Ws, queueFile), "utf8");
    const queueEnd = content.trim().split("\n").filter(Boolean);
    expect(queueEnd).toEqual([]);
    },
    30000  // 30 second timeout for Jest
  );
});
