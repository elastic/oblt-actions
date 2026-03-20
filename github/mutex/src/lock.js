const core = require("@actions/core");
const fs = require("fs");
const { setUpRepo, enqueue, waitForLock } = require("./utils");

async function run() {
  const branch = core.getInput("branch");
  const checkoutLocation = core.getInput("internal_checkout-location");
  const githubServer = core.getInput("github_server");
  const repository = core.getInput("repository");
  const repoToken = core.getInput("repo-token");
  const suffix = core.getInput("suffix");
  const timeoutMinutes = parseInt(core.getInput("timeout-minutes") || "30", 10);

  if (isNaN(timeoutMinutes) || timeoutMinutes <= 0) {
    core.setFailed("timeout-minutes must be a positive integer");
    return;
  }

  const queueFile = "mutex_queue";
  const repoUrl = `https://x-access-token:${repoToken}@${githubServer}/${repository}`;
  const ticketId = `${process.env.GITHUB_RUN_ID}-${Date.now()}-${Math.floor(Math.random() * 1000)}-${suffix}`;

  core.saveState("ticket_id", ticketId);

  core.info(
    `Cloning and checking out ${repository}:${branch} in ${checkoutLocation}`
  );

  fs.mkdirSync(checkoutLocation, { recursive: true });

  await setUpRepo(repoUrl, checkoutLocation);
  await enqueue(branch, queueFile, ticketId, checkoutLocation, timeoutMinutes);
  await waitForLock(branch, queueFile, ticketId, checkoutLocation, timeoutMinutes);

  core.info("Lock successfully acquired");
}

run().catch((error) => {
  core.setFailed(error.message);
});
