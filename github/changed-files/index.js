// https://github.com/kandhavivekraj/git-changed-files
const gitChangedFiles = require("./git-changed-files");
const core = require("@actions/core");

async function run() {
  added = [];
  modified = [];
  deleted = [];
  baseBranch = core.getInput("baseRef") || "main";
  head = core.getInput("ref") || "HEAD";
  filter = JSON.parse(core.getInput("filter")||'["*.*"]');
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
    core.setOutput("added", JSON.stringify(added));
    core.setOutput("modified", JSON.stringify(modified));
    core.setOutput("deleted", JSON.stringify(deleted));
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

module.exports = run;
