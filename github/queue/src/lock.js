const core = require("@actions/core");
const fs = require("fs");
const {
  setUpRepo,
  enqueue,
  waitForSlot,
  getQueueRepoPath,
  createRequesterId,
} = require("./utils");

async function run() {
  const branch = core.getInput("branch") || "job-queue";
  const checkoutLocation = getQueueRepoPath();
  const githubServer = "github.com";
  const repository = core.getInput("repository");
  const repoToken = core.getInput("github-token");
  const suffix = core.getInput("suffix") || "default";
  const queueFile = core.getInput("queue-file") || "job_queue";
  const concurrencyLimit = parseInt(core.getInput("concurrency-limit") || "50", 10);
  const maxQueueSize = parseInt(core.getInput("max-queue-size") || "50", 10);
  const syncRuns = core.getBooleanInput("sync-runs");
  const timeoutMinutes = parseInt(core.getInput("timeout-minutes") || "30", 10);

  if (isNaN(timeoutMinutes) || timeoutMinutes <= 0) {
    core.setFailed("timeout-minutes must be a positive integer");
    return;
  }
  if (isNaN(concurrencyLimit) || concurrencyLimit <= 0) {
    core.setFailed("concurrency-limit must be a positive integer");
    return;
  }

  const repoUrl = `https://x-access-token:${repoToken}@${githubServer}/${repository}`;
  const requesterId = createRequesterId(suffix);
  const enqueueTimeoutMinutes = 5;

  core.saveState("requester_id", requesterId);
  core.saveState("branch", branch);
  core.saveState("queue_file", queueFile);
  core.saveState("repository", repository);
  core.saveState("timeout_minutes", timeoutMinutes.toString());

  core.info(
    `Cloning and checking out ${repository}:${branch} in ${checkoutLocation} for requester [${requesterId}]`
  );

  fs.mkdirSync(checkoutLocation, { recursive: true });

  await setUpRepo(repoUrl, checkoutLocation);
  await enqueue(
    branch,
    queueFile,
    requesterId,
    checkoutLocation,
    enqueueTimeoutMinutes,
    concurrencyLimit,
    maxQueueSize,
    syncRuns,
    repository,
    repoToken
  );
  await waitForSlot(
    branch,
    queueFile,
    requesterId,
    checkoutLocation,
    timeoutMinutes,
    concurrencyLimit,
    syncRuns,
    repository,
    repoToken
  );

  core.info("Execution slot successfully acquired");
}

run().catch((error) => {
  core.setFailed(error.message);
});
