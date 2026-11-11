const core = require("@actions/core");
const fs = require("fs");
const { setUpRepo, dequeue, getQueueRepoPath } = require("./utils");

async function run() {
  const branch = core.getState("branch") || core.getInput("branch") || "job-queue";
  const checkoutLocation = getQueueRepoPath();
  const githubServer = "github.com";
  const repository = core.getState("repository") || core.getInput("repository");
  const repoToken = core.getInput("github-token");
  const queueFile = core.getState("queue_file") || core.getInput("queue-file") || "job_queue";
  const timeoutMinutes = parseInt(
    core.getState("timeout_minutes") || core.getInput("timeout-minutes") || "30",
    10
  );

  if (isNaN(timeoutMinutes) || timeoutMinutes <= 0) {
    core.setFailed("timeout-minutes must be a positive integer");
    return;
  }

  const repoUrl = `https://x-access-token:${repoToken}@${githubServer}/${repository}`;
  const requesterId = core.getState("requester_id");

  if (!requesterId) {
    core.info("No requester_id saved in state, skipping dequeue");
    return;
  }

  fs.mkdirSync(checkoutLocation, { recursive: true });

  await setUpRepo(repoUrl, checkoutLocation);
  await dequeue(branch, queueFile, requesterId, checkoutLocation, timeoutMinutes);

  core.info("Successfully released slot and dequeued");
}

run().catch((error) => {
  core.setFailed(error.message);
});
