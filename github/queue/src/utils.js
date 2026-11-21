const fs = require("fs");
const path = require("path");
const https = require("https");
const core = require("@actions/core");
const simpleGit = require("simple-git");

const ENQUEUE_PUSH_RETRY_DELAY_MS = 1000;
const LOCK_POLL_DELAY_MS = 5000;
const SYNC_MAX_RETRIES = 10;
const SYNC_RETRY_BACKOFF_MS = 200; // Start at 200ms, exponential backoff

function getQueueRepoPath() {
  const runnerTemp = process.env.RUNNER_TEMP ?? "/tmp";
  const runAttempt = process.env.GITHUB_RUN_ATTEMPT ?? "1";
  const runId = process.env.GITHUB_RUN_ID ?? "local";

  return path.join(runnerTemp, "queue", `${runId}-${runAttempt}`, "repo");
}

function createDeadline(timeoutMinutes) {
  const startTime = Date.now();
  return {
    endTime: startTime + timeoutMinutes * 60 * 1000,
    startTime,
    timeoutMinutes,
  };
}

function checkTimeout(deadline, requesterId, operation) {
  if (Date.now() >= deadline.endTime) {
    const elapsedMinutes = Math.round((Date.now() - deadline.startTime) / 60000);
    throw new Error(
      `[${requesterId}] ${operation} timed out after ${elapsedMinutes} minutes (limit: ${deadline.timeoutMinutes})`
    );
  }
}

function readQueue(queuePath) {
  if (!fs.existsSync(queuePath)) return [];
  return fs.readFileSync(queuePath, "utf8").split("\n").filter((l) => l.trim().length > 0);
}

function writeQueue(queuePath, lines) {
  fs.writeFileSync(queuePath, lines.length > 0 ? lines.join("\n") + "\n" : "");
}

/**
 * Format requesterId embedding the GitHub Run ID:
 * Format: run_id:run_attempt:suffix:timestamp_hash
 */
function createRequesterId(suffix) {
  const runId = process.env.GITHUB_RUN_ID ?? "local";
  const runAttempt = process.env.GITHUB_RUN_ATTEMPT ?? "1";
  const rand = Math.floor(Math.random() * 1000);
  return `${runId}:${runAttempt}:${suffix}:${Date.now()}-${rand}`;
}

function parseRunIdFromRequesterId(requesterId) {
  if (!requesterId) return null;
  const parts = requesterId.split(":");
  return parts[0] || null;
}

async function setUpRepo(repoUrl, cwd) {
  const git = simpleGit(cwd);

  await git.init();
  await git.addConfig("user.name", "github-bot");
  await git.addConfig("user.email", "github-bot@users.noreply.github.com");

  try {
    await git.removeRemote("origin");
  } catch (e) {
    core.debug(`Remove existing remote failed: ${e.message}`);
  }

  await git.addRemote("origin", repoUrl);
}

/**
 * Synchronize local branch with remote with exponential backoff & jitter.
 */
async function syncBranch(branch, git, deadline, requesterId) {
  let retryCount = 0;

  while (true) {
    try {
      if (Date.now() >= deadline.endTime) {
        const elapsed = Math.round((Date.now() - deadline.startTime) / 60000);
        throw new Error(`[${requesterId}] Branch sync timeout after ${elapsed} minutes`);
      }

      try {
        await git.reset(["--hard", "--quiet"]);
        await git.clean("f", ["-d", "--quiet"]);
      } catch (e) {
        core.debug(`[${requesterId}] Cleanup failed: ${e.message}`);
      }

      try {
        await git.branch(["-D", branch, "-q"]);
      } catch (e) {
        core.debug(`[${requesterId}] Delete branch failed: ${e.message}`);
      }

      try {
        await git.fetch(["origin", branch, "-q"]);
      } catch (e) {
        core.debug(`[${requesterId}] Fetch failed: ${e.message}`);
      }

      try {
        await git.checkout(["-B", branch, `origin/${branch}`, "-q"]);
        core.debug(`[${requesterId}] Created/reset tracking branch ${branch}`);
      } catch (trackingErr) {
        try {
          await git.checkout(["-q", "--orphan", branch]);
          core.debug(`[${requesterId}] Created orphan branch ${branch}`);
        } catch (orphanErr) {
          throw new Error(
            `Checkout failed: tracking (${trackingErr.message}), orphan (${orphanErr.message})`
          );
        }
      }

      return;
    } catch (error) {
      retryCount++;
      if (retryCount >= SYNC_MAX_RETRIES) {
        core.error(`[${requesterId}] Branch sync failed after ${SYNC_MAX_RETRIES} retries: ${error.message}`);
        throw error;
      }

      // Add jitter: ±25% random spread
      const baseDelay = SYNC_RETRY_BACKOFF_MS * Math.pow(2, retryCount - 1);
      const jitter = baseDelay * (0.75 + Math.random() * 0.5);
      const delayMs = Math.round(jitter);

      core.warning(
        `[${requesterId}] Sync attempt ${retryCount} failed: ${error.message}. Retrying in ${delayMs}ms...`
      );
      sleep(delayMs);
    }
  }
}

/**
 * Check run status via GitHub REST API.
 * Returns true if the run is completed / cancelled / not found (i.e. dead).
 */
function fetchRunStatus(repository, runId, token) {
  return new Promise((resolve) => {
    if (!token || !runId || runId === "local" || isNaN(Number(runId))) {
      return resolve(null);
    }

    const options = {
      hostname: "api.github.com",
      path: `/repos/${repository}/actions/runs/${runId}`,
      method: "GET",
      headers: {
        "User-Agent": "github-queue-action",
        Authorization: `Bearer ${token}`,
        Accept: "application/vnd.github+json",
      },
    };

    const req = https.request(options, (res) => {
      let data = "";
      res.on("data", (chunk) => (data += chunk));
      res.on("end", () => {
        if (res.statusCode === 200) {
          try {
            const json = JSON.parse(data);
            resolve(json.status); // e.g. "queued", "in_progress", "completed"
          } catch (e) {
            resolve(null);
          }
        } else if (res.statusCode === 404) {
          resolve("not_found");
        } else {
          resolve(null);
        }
      });
    });

    req.on("error", () => resolve(null));
    req.setTimeout(5000, () => {
      req.destroy();
      resolve(null);
    });
    req.end();
  });
}

/**
 * Prune dead runs from queue list
 */
async function pruneDeadRuns(lines, repository, token, currentRunId) {
  const activeLines = [];
  let cleanedCount = 0;

  for (const item of lines) {
    const itemRunId = parseRunIdFromRequesterId(item);
    if (!itemRunId || itemRunId === currentRunId || itemRunId === "local") {
      activeLines.push(item);
      continue;
    }

    const status = await fetchRunStatus(repository, itemRunId, token);
    if (status === "completed" || status === "not_found") {
      core.info(`Pruning dead/completed run [${itemRunId}] item: ${item}`);
      cleanedCount++;
    } else {
      activeLines.push(item);
    }
  }

  return { activeLines, cleanedCount };
}

async function enqueue(
  branch,
  queueFile,
  requesterId,
  cwd,
  timeoutMinutes,
  concurrencyLimit = 50,
  maxQueueSize = 50,
  syncRuns = true,
  repository = "",
  token = ""
) {
  const deadline = createDeadline(timeoutMinutes);
  const git = simpleGit(cwd);
  const queuePath = path.join(cwd, queueFile);
  const currentRunId = parseRunIdFromRequesterId(requesterId);

  core.info(`[${requesterId}] Enqueuing to branch ${branch}, file ${queueFile}`);

  while (true) {
    checkTimeout(deadline, requesterId, "Enqueue");
    await syncBranch(branch, git, deadline, requesterId);

    let lines = readQueue(queuePath);

    // Only prune stale runs if enabled AND queue has reached running capacity (concurrencyLimit)
    if (syncRuns && repository && token && lines.length >= concurrencyLimit) {
      try {
        // Inspect only the first `concurrencyLimit` items which are holding running slots
        const runningItems = lines.slice(0, concurrencyLimit);
        const { activeLines: activeRunning, cleanedCount } = await pruneDeadRuns(runningItems, repository, token, currentRunId);
        if (cleanedCount > 0) {
          lines = [...activeRunning, ...lines.slice(concurrencyLimit)];
          writeQueue(queuePath, lines);
        }
      } catch (err) {
        core.debug(`Failed to prune dead runs: ${err.message}`);
      }
    }

    if (lines.includes(requesterId)) break;

    // Check capacity limit: running (concurrencyLimit) + waiting (maxQueueSize)
    if (maxQueueSize > 0) {
      const maxTotalCapacity = concurrencyLimit + maxQueueSize;
      if (lines.length >= maxTotalCapacity) {
        core.warning(
          `[${requesterId}] Queue is at max capacity (${lines.length}/${maxTotalCapacity}). Waiting before enqueuing...`
        );
        sleep(LOCK_POLL_DELAY_MS);
        continue;
      }
    }

    core.info(`[${requesterId}] Adding ourselves to the queue file ${queueFile}`);
    writeQueue(queuePath, [...lines, requesterId]);

    await git.add(queueFile);
    await git.commit(`[${requesterId}] Enqueue`, ["-q"]);

    try {
      await git.push(["--set-upstream", "origin", branch, "-q"]);
      break;
    } catch (e) {
      core.warning(`[${requesterId}] Enqueue push failed: ${e.message}`);
      core.warning(`[${requesterId}] Fetching latest remote state and resetting`);
      try {
        await git.fetch(["origin", branch, "-q"]);
        await git.reset(["--hard", `origin/${branch}`]);
      } catch (resetErr) {
        core.warning(`[${requesterId}] Reset failed: ${resetErr.message}`);
      }
      checkTimeout(deadline, requesterId, "Enqueue push retry");
      const jitter = ENQUEUE_PUSH_RETRY_DELAY_MS * (0.8 + Math.random() * 0.4);
      sleep(jitter);
    }
  }
}

async function waitForSlot(
  branch,
  queueFile,
  requesterId,
  cwd,
  timeoutMinutes,
  concurrencyLimit = 50,
  syncRuns = true,
  repository = "",
  token = ""
) {
  const deadline = createDeadline(timeoutMinutes);
  const git = simpleGit(cwd);
  const queuePath = path.join(cwd, queueFile);
  const currentRunId = parseRunIdFromRequesterId(requesterId);

  while (true) {
    checkTimeout(deadline, requesterId, "WaitForSlot");
    await syncBranch(branch, git, deadline, requesterId);

    const stat = fs.statSync(queuePath, { throwIfNoEntry: false });
    if (!stat || stat.size === 0) {
      core.info(`[${requesterId}] ${queueFile} unexpectedly empty, continuing`);
      break;
    }

    let lines = readQueue(queuePath);

    const position = lines.indexOf(requesterId);
    if (position === -1) {
      core.warning(`[${requesterId}] Not found in queue file. Re-enqueuing or continuing.`);
      break;
    }

    if (position < concurrencyLimit) {
      core.info(
        `[${requesterId}] Slot acquired! Queue position ${position + 1} is within concurrency limit (${concurrencyLimit}).`
      );
      break;
    }

    // Prune stale runs only when waiting in queue (i.e. running limit reached)
    // and only check the active running items (index 0 to concurrencyLimit) to save API calls
    if (syncRuns && repository && token) {
      try {
        const runningItems = lines.slice(0, concurrencyLimit);
        const { activeLines: activeRunning, cleanedCount } = await pruneDeadRuns(runningItems, repository, token, currentRunId);
        if (cleanedCount > 0) {
          lines = [...activeRunning, ...lines.slice(concurrencyLimit)];
          writeQueue(queuePath, lines);
          await git.add(queueFile);
          await git.commit(`[${requesterId}] Pruned ${cleanedCount} dead runs`, ["-q"]);
          try {
            await git.push(["--set-upstream", "origin", branch, "-q"]);
          } catch (e) {
            core.debug(`Failed to push dead run cleanup: ${e.message}`);
          }
        }
      } catch (err) {
        core.debug(`Dead run prune error during poll: ${err.message}`);
      }
    }

    core.info(
      `[${requesterId}] Waiting for available slot. Current position: ${position + 1}/${lines.length} (limit: ${concurrencyLimit})`
    );
    checkTimeout(deadline, requesterId, "WaitForSlot poll");
    sleep(LOCK_POLL_DELAY_MS);
  }
}

async function dequeue(branch, queueFile, requesterId, cwd, timeoutMinutes) {
  const deadline = createDeadline(timeoutMinutes);
  const git = simpleGit(cwd);
  const queuePath = path.join(cwd, queueFile);

  while (true) {
    checkTimeout(deadline, requesterId, "Dequeue");
    await syncBranch(branch, git, deadline, requesterId);

    const lines = readQueue(queuePath);

    if (!lines.includes(requesterId)) {
      core.info(`[${requesterId}] Not in queue (likely already removed by concurrent dequeue) - exiting`);
      break;
    }

    core.info(`[${requesterId}] Dequeueing and releasing slot`);
    writeQueue(queuePath, lines.filter((l) => l !== requesterId));

    await git.add(queueFile);
    await git.commit(`[${requesterId}] Release slot`, ["-q"]);

    try {
      await git.push(["--set-upstream", "origin", branch, "-q"]);
      break;
    } catch (e) {
      core.warning(`[${requesterId}] Dequeue push failed: ${e.message}`);
      try {
        await git.fetch(["origin", branch, "-q"]);
        await git.reset(["--hard", `origin/${branch}`]);
      } catch (resetErr) {
        core.warning(`[${requesterId}] Reset failed: ${resetErr.message}`);
      }
      checkTimeout(deadline, requesterId, "Dequeue push retry");
      const jitter = LOCK_POLL_DELAY_MS * (0.8 + Math.random() * 0.4);
      sleep(jitter);
    }
  }
}

function sleep(ms) {
  Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, ms);
}

module.exports = {
  setUpRepo,
  syncBranch,
  enqueue,
  waitForSlot,
  dequeue,
  getQueueRepoPath,
  createRequesterId,
  parseRunIdFromRequesterId,
  pruneDeadRuns,
  fetchRunStatus,
};
