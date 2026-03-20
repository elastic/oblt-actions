const fs = require("fs");
const path = require("path");
const core = require("@actions/core");
const simpleGit = require("simple-git");

const ENQUEUE_PUSH_RETRY_DELAY_MS = 1000;
const LOCK_POLL_DELAY_MS = 5000;

function createDeadline(timeoutMinutes) {
  const startTime = Date.now();
  return {
    endTime: startTime + timeoutMinutes * 60 * 1000,
    startTime,
    timeoutMinutes,
  };
}

function checkTimeout(deadline, ticketId, operation) {
  if (Date.now() >= deadline.endTime) {
    const elapsedMinutes = Math.round((Date.now() - deadline.startTime) / 60000);
    throw new Error(
      `[${ticketId}] ${operation} timed out after ${elapsedMinutes} minutes (limit: ${deadline.timeoutMinutes})`,
    );
  }
}

function readQueue(queuePath) {
  if (!fs.existsSync(queuePath)) return [];
  return fs.readFileSync(queuePath, "utf8").split("\n").filter((l) => l.length > 0);
}

function writeQueue(queuePath, lines) {
  fs.writeFileSync(queuePath, lines.length > 0 ? lines.join("\n") + "\n" : "");
}

async function setUpRepo(repoUrl, cwd) {
  const git = simpleGit(cwd);

  await git.init();
  await git.addConfig("user.name", "github-bot");
  await git.addConfig("user.email", "github-bot@users.noreply.github.com");

  try {
    await git.removeRemote("origin");
  } catch (e) {
    core.debug(`Remove existing remote failed (expected if remote doesn't exist): ${e.message}`);
  }

  await git.addRemote("origin", repoUrl);
}

async function updateBranch(branch, git) {
  const tempBranch = `mutex/temp-branch-${Date.now()}`;
  // Clear any uncommitted changes in working directory before checkout
  await git.reset(["--hard", "-q"]);
  await git.checkout(["-q", "--orphan", tempBranch]);

  try {
    await git.branch(["-D", branch]);
  } catch (e) {
    core.debug(`Branch delete failed (expected if branch doesn't exist): ${e.message}`);
  }

  try {
    await git.fetch(["origin", branch, "-q"]);
  } catch (e) {
    core.debug(`Fetch failed (expected for new mutex): ${e.message}`);
  }

  try {
    await git.checkout([branch, "-q"]);
  } catch {
    // If branch doesn't exist locally, create a proper tracking branch from remote
    await git.checkout(["-b", branch, `origin/${branch}`, "-q"]);
  }
}

async function enqueue(branch, queueFile, ticketId, cwd, timeoutMinutes) {
  const deadline = createDeadline(timeoutMinutes);
  const git = simpleGit(cwd);
  const queuePath = path.join(cwd, queueFile);

  core.info(`[${ticketId}] Enqueuing to branch ${branch}, file ${queueFile}`);

  while (true) {
    checkTimeout(deadline, ticketId, "Enqueue");
    await updateBranch(branch, git);

    const lines = readQueue(queuePath);
    if (lines.includes(ticketId)) break;

    core.info(`[${ticketId}] Adding ourself to the queue file ${queueFile}`);
    writeQueue(queuePath, [...lines, ticketId]);

    await git.add(queueFile);
    await git.commit(`[${ticketId}] Enqueue `, ["-q"]);

    try {
      await git.push(["--set-upstream", "origin", branch, "-q"]);
      break;
    } catch (e) {
      core.error(`[${ticketId}] Enqueue push failed: ${e.message}`);
      core.error(`[${ticketId}] Fetching latest remote state and resetting - queue may have changed during concurrent enqueue`);
      try {
        await git.fetch(["origin", branch, "-q"]);
        await git.reset(["--hard", `origin/${branch}`]);
      } catch (resetErr) {
        core.error(`[${ticketId}] Reset failed: ${resetErr.message}`);
      }
      checkTimeout(deadline, ticketId, "Enqueue push retry");
      sleep(ENQUEUE_PUSH_RETRY_DELAY_MS);
    }
  }
}

async function waitForLock(branch, queueFile, ticketId, cwd, timeoutMinutes) {
  const deadline = createDeadline(timeoutMinutes);
  const git = simpleGit(cwd);
  const queuePath = path.join(cwd, queueFile);

  while (true) {
    checkTimeout(deadline, ticketId, "WaitForLock");
    await updateBranch(branch, git);

    const stat = fs.statSync(queuePath, { throwIfNoEntry: false });
    if (!stat || stat.size === 0) {
      core.info(`[${ticketId}] ${queueFile} unexpectedly empty, continuing`);
      break;
    }

    const lines = readQueue(queuePath);
    if (lines[0] === ticketId) break;

    core.info(`[${ticketId}] Waiting for lock - Current lock assigned to [${lines[0]}]`);
    checkTimeout(deadline, ticketId, "WaitForLock poll");
    sleep(LOCK_POLL_DELAY_MS);
  }
}

async function dequeue(branch, queueFile, ticketId, cwd, timeoutMinutes) {
  const deadline = createDeadline(timeoutMinutes);
  const git = simpleGit(cwd);
  const queuePath = path.join(cwd, queueFile);

  while (true) {
    checkTimeout(deadline, ticketId, "Dequeue");
    await updateBranch(branch, git);

    const lines = readQueue(queuePath);
    let message;

    if (lines.length > 0 && lines[0] === ticketId) {
      core.info(`[${ticketId}] Unlocking`);
      message = `[${ticketId}] Unlock`;
      writeQueue(queuePath, lines.slice(1));
    } else if (lines.includes(ticketId)) {
      core.info(`[${ticketId}] Dequeueing. We don't have the lock!`);
      message = `[${ticketId}] Dequeue`;
      writeQueue(queuePath, lines.filter((l) => l !== ticketId));
    } else {
      // Job not in queue - likely removed by concurrent dequeue operation
      // This is not an error, just exit successfully
      core.info(`[${ticketId}] Not in queue (likely already removed by concurrent dequeue) - exiting`);
      break;
    }

    await git.add(queueFile);
    await git.commit(message, ["-q"]);

    try {
      await git.push(["--set-upstream", "origin", branch, "-q"]);
      break;
    } catch (e) {
      core.warning(`[${ticketId}] Dequeue push failed: ${e.message}`);
      core.warning(`[${ticketId}] Fetching latest remote state and resetting - queue may have changed during concurrent dequeue`);
      // Fetch latest remote state before resetting
      try {
        await git.fetch(["origin", branch, "-q"]);
        await git.reset(["--hard", `origin/${branch}`]);
      } catch (resetErr) {
        core.warning(`[${ticketId}] Reset failed: ${resetErr.message}`);
      }
      checkTimeout(deadline, ticketId, "Dequeue push retry");
      sleep(LOCK_POLL_DELAY_MS);
    }
  }
}

function sleep(ms) {
  Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, ms);
}

module.exports = {
  setUpRepo,
  updateBranch,
  enqueue,
  waitForLock,
  dequeue,
};
