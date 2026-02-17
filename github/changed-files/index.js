// https://github.com/kandhavivekraj/git-changed-files
import gitChangedFiles from "./git-changed-files/index.js";
import * as core from "@actions/core";

async function run() {
  let added = [];
  let modified = [];
  let deleted = [];
  let baseBranch = core.getInput("base-ref") || "main";
  let head = core.getInput("ref") || "HEAD";
  let filter = JSON.parse(core.getInput("filter")||'["*.*"]');
  try {
    let committedGitFiles = await gitChangedFiles({
      baseBranch: baseBranch,
      head: head,
      formats: filter,
      showStatus: true,
    });
    core.info(JSON.stringify(committedGitFiles));
    committedGitFiles["committedFiles"].forEach((file) => {
      if (file.status === "Added") {
        added.push(file.filename);
      }
      if (file.status === "Modified") {
        modified.push(file.filename);
      }
      if (file.status === "Deleted") {
        deleted.push(file.filename);
      }
    });
    core.info("Added Files: " + JSON.stringify(added));
    core.info("Modified Files: " + JSON.stringify(modified));
    core.info("Deleted Files: " + JSON.stringify(deleted));
    core.info("Changed Files: " + JSON.stringify(added.concat(modified, deleted)));
    core.setOutput("added", JSON.stringify(added));
    core.setOutput("modified", JSON.stringify(modified));
    core.setOutput("deleted", JSON.stringify(deleted));
    core.setOutput("changed", JSON.stringify(added.concat(modified, deleted)));
    core.setOutput("count", added.length + modified.length + deleted.length);
    core.setOutput("count-added", added.length);
    core.setOutput("count-modified", modified.length);
    core.setOutput("count-deleted", deleted.length);
  } catch(err){
    core.error(err);
    core.setFailed(err.message);
  };
}

run();

export default run;
