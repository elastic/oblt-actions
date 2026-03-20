const core = require("@actions/core");
const fs = require("fs");
const { setUpRepo, dequeue } = require("./utils");

async function run() {
  const branch = core.getInput("branch");
  const checkoutLocation = core.getInput("internal_checkout-location");
  const githubServer = core.getInput("github_server");
  const repository = core.getInput("repository");
  const repoToken = core.getInput("repo-token");
  const timeoutMinutes = parseInt(core.getInput("timeout-minutes") || "30", 10);

  if (isNaN(timeoutMinutes) || timeoutMinutes <= 0) {
    core.setFailed("timeout-minutes must be a positive integer");
    return;
  }

  const queueFile = "mutex_queue";
  const repoUrl = `https://x-access-token:${repoToken}@${githubServer}/${repository}`;
  const ticketId = core.getState("ticket_id");

  fs.mkdirSync(checkoutLocation, { recursive: true });

  await setUpRepo(repoUrl, checkoutLocation);
  await dequeue(branch, queueFile, ticketId, checkoutLocation, timeoutMinutes);

  core.info("Successfully unlocked");
}

run().catch((error) => {
  core.setFailed(error.message);
});
