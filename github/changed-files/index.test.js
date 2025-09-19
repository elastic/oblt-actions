// github/changed-files/index.test.js
const run = require("./index");
const gitChangedFiles = require("./git-changed-files");
const core = require("@actions/core");

jest.mock("./git-changed-files");
jest.mock("@actions/core");

describe("run", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("should call gitChangedFiles with correct parameters and set outputs", async () => {
    const mockCommittedFiles = {
      committedFiles: [
        { filename: "file1.txt", status: "Added" },
        { filename: "file2.js", status: "Modified" },
        { filename: "file3.md", status: "Deleted" },
        { filename: "file4.txt", status: "Added" },
      ],
    };
    gitChangedFiles.mockResolvedValue(mockCommittedFiles);
    core.getInput.mockReturnValueOnce("develop").mockReturnValueOnce("my-branch").mockReturnValueOnce('["*.txt", "*.js"]');

    await run();

    expect(gitChangedFiles).toHaveBeenCalledWith({
      baseBranch: "develop",
      head: "my-branch",
      formats: ["*.txt", "*.js"],
      showStatus: true,
    });
    expect(core.info).toHaveBeenCalledWith(JSON.stringify(mockCommittedFiles));
    expect(core.info).toHaveBeenCalledWith(
      "Added Files: " + JSON.stringify(["file1.txt", "file4.txt"])
    );
    expect(core.info).toHaveBeenCalledWith(
      "Modified Files: " + JSON.stringify(["file2.js"])
    );
    expect(core.info).toHaveBeenCalledWith(
      "Deleted Files: " + JSON.stringify(["file3.md"])
    );
    expect(core.info).toHaveBeenCalledWith(
      "Changed Files: " + JSON.stringify(["file1.txt", "file4.txt", "file2.js", "file3.md"])
    );
    expect(core.setOutput).toHaveBeenCalledWith(
      "added",
      JSON.stringify(["file1.txt", "file4.txt"])
    );
    expect(core.setOutput).toHaveBeenCalledWith(
      "modified",
      JSON.stringify(["file2.js"])
    );
    expect(core.setOutput).toHaveBeenCalledWith(
      "deleted",
      JSON.stringify(["file3.md"])
    );
    expect(core.setOutput).toHaveBeenCalledWith(
      "changed",
      JSON.stringify(["file1.txt", "file4.txt", "file2.js", "file3.md"])
    );
    expect(core.setOutput).toHaveBeenCalledWith("count", 4);
    expect(core.setOutput).toHaveBeenCalledWith("count-added", 2);
    expect(core.setOutput).toHaveBeenCalledWith("count-modified", 1);
    expect(core.setOutput).toHaveBeenCalledWith("count-deleted", 1);
  });

  it("should use default values for base-ref, ref and filter if not provided", async () => {
    const mockCommittedFiles = {
      committedFiles: [],
    };
    gitChangedFiles.mockResolvedValue(mockCommittedFiles);
    core.getInput.mockReturnValueOnce(undefined).mockReturnValueOnce(undefined).mockReturnValueOnce(undefined);

    await run();

    expect(gitChangedFiles).toHaveBeenCalledWith({
      baseBranch: "main",
      head: "HEAD",
      formats: ["*.*"],
      showStatus: true,
    });
  });

  it("should handle errors and set failed status", async () => {
    const errorMessage = "Something went wrong";
    const error = new Error(errorMessage);
    gitChangedFiles.mockRejectedValue(error);
    core.getInput.mockReturnValueOnce("main").mockReturnValueOnce("HEAD").mockReturnValueOnce('["*.*"]');

    await run();

    expect(core.error).toHaveBeenCalledWith(error);
    expect(core.setFailed).toHaveBeenCalledWith(errorMessage);
  });

  it("should handle empty committed files", async () => {
    const mockCommittedFiles = {
      committedFiles: [],
    };
    gitChangedFiles.mockResolvedValue(mockCommittedFiles);
    core.getInput.mockReturnValueOnce("main").mockReturnValueOnce("HEAD").mockReturnValueOnce('["*.*"]');

    await run();

    expect(core.info).toHaveBeenCalledWith(JSON.stringify(mockCommittedFiles));
    expect(core.info).toHaveBeenCalledWith("Added Files: " + JSON.stringify([]));
    expect(core.info).toHaveBeenCalledWith("Modified Files: " + JSON.stringify([]));
    expect(core.info).toHaveBeenCalledWith("Deleted Files: " + JSON.stringify([]));
    expect(core.info).toHaveBeenCalledWith("Changed Files: " + JSON.stringify([]));
    expect(core.setOutput).toHaveBeenCalledWith("added", JSON.stringify([]));
    expect(core.setOutput).toHaveBeenCalledWith("modified", JSON.stringify([]));
    expect(core.setOutput).toHaveBeenCalledWith("deleted", JSON.stringify([]));
    expect(core.setOutput).toHaveBeenCalledWith("changed", JSON.stringify([]));
    expect(core.setOutput).toHaveBeenCalledWith("count", 0);
    expect(core.setOutput).toHaveBeenCalledWith("count-added", 0);
    expect(core.setOutput).toHaveBeenCalledWith("count-modified", 0);
    expect(core.setOutput).toHaveBeenCalledWith("count-deleted", 0);
  });
});
