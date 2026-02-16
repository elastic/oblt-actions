// github/changed-files/index.test.js
import { jest, describe, it, expect, beforeEach } from '@jest/globals';

// Create mocks before importing modules
const mockGitChangedFiles = jest.fn();
const mockCore = {
  getInput: jest.fn(),
  info: jest.fn(),
  setOutput: jest.fn(),
  error: jest.fn(),
  setFailed: jest.fn(),
};

// Mock the modules
jest.unstable_mockModule("./git-changed-files/index.js", () => ({
  default: mockGitChangedFiles,
}));

jest.unstable_mockModule("@actions/core", () => mockCore);

// Import after mocking
const { default: run } = await import("./index.js");

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
    mockGitChangedFiles.mockResolvedValue(mockCommittedFiles);
    mockCore.getInput.mockReturnValueOnce("develop").mockReturnValueOnce("my-branch").mockReturnValueOnce('["*.txt", "*.js"]');

    await run();

    expect(mockGitChangedFiles).toHaveBeenCalledWith({
      baseBranch: "develop",
      head: "my-branch",
      formats: ["*.txt", "*.js"],
      showStatus: true,
    });
    expect(mockCore.info).toHaveBeenCalledWith(JSON.stringify(mockCommittedFiles));
    expect(mockCore.info).toHaveBeenCalledWith(
      "Added Files: " + JSON.stringify(["file1.txt", "file4.txt"])
    );
    expect(mockCore.info).toHaveBeenCalledWith(
      "Modified Files: " + JSON.stringify(["file2.js"])
    );
    expect(mockCore.info).toHaveBeenCalledWith(
      "Deleted Files: " + JSON.stringify(["file3.md"])
    );
    expect(mockCore.info).toHaveBeenCalledWith(
      "Changed Files: " + JSON.stringify(["file1.txt", "file4.txt", "file2.js", "file3.md"])
    );
    expect(mockCore.setOutput).toHaveBeenCalledWith(
      "added",
      JSON.stringify(["file1.txt", "file4.txt"])
    );
    expect(mockCore.setOutput).toHaveBeenCalledWith(
      "modified",
      JSON.stringify(["file2.js"])
    );
    expect(mockCore.setOutput).toHaveBeenCalledWith(
      "deleted",
      JSON.stringify(["file3.md"])
    );
    expect(mockCore.setOutput).toHaveBeenCalledWith(
      "changed",
      JSON.stringify(["file1.txt", "file4.txt", "file2.js", "file3.md"])
    );
    expect(mockCore.setOutput).toHaveBeenCalledWith("count", 4);
    expect(mockCore.setOutput).toHaveBeenCalledWith("count-added", 2);
    expect(mockCore.setOutput).toHaveBeenCalledWith("count-modified", 1);
    expect(mockCore.setOutput).toHaveBeenCalledWith("count-deleted", 1);
  });

  it("should use default values for base-ref, ref and filter if not provided", async () => {
    const mockCommittedFiles = {
      committedFiles: [],
    };
    mockGitChangedFiles.mockResolvedValue(mockCommittedFiles);
    mockCore.getInput.mockReturnValueOnce(undefined).mockReturnValueOnce(undefined).mockReturnValueOnce(undefined);

    await run();

    expect(mockGitChangedFiles).toHaveBeenCalledWith({
      baseBranch: "main",
      head: "HEAD",
      formats: ["*.*"],
      showStatus: true,
    });
  });

  it("should handle errors and set failed status", async () => {
    const errorMessage = "Something went wrong";
    const error = new Error(errorMessage);
    mockGitChangedFiles.mockRejectedValue(error);
    mockCore.getInput.mockReturnValueOnce("main").mockReturnValueOnce("HEAD").mockReturnValueOnce('["*.*"]');

    await run();

    expect(mockCore.error).toHaveBeenCalledWith(error);
    expect(mockCore.setFailed).toHaveBeenCalledWith(errorMessage);
  });

  it("should handle empty committed files", async () => {
    const mockCommittedFiles = {
      committedFiles: [],
    };
    mockGitChangedFiles.mockResolvedValue(mockCommittedFiles);
    mockCore.getInput.mockReturnValueOnce("main").mockReturnValueOnce("HEAD").mockReturnValueOnce('["*.*"]');

    await run();

    expect(mockCore.info).toHaveBeenCalledWith(JSON.stringify(mockCommittedFiles));
    expect(mockCore.info).toHaveBeenCalledWith("Added Files: " + JSON.stringify([]));
    expect(mockCore.info).toHaveBeenCalledWith("Modified Files: " + JSON.stringify([]));
    expect(mockCore.info).toHaveBeenCalledWith("Deleted Files: " + JSON.stringify([]));
    expect(mockCore.info).toHaveBeenCalledWith("Changed Files: " + JSON.stringify([]));
    expect(mockCore.setOutput).toHaveBeenCalledWith("added", JSON.stringify([]));
    expect(mockCore.setOutput).toHaveBeenCalledWith("modified", JSON.stringify([]));
    expect(mockCore.setOutput).toHaveBeenCalledWith("deleted", JSON.stringify([]));
    expect(mockCore.setOutput).toHaveBeenCalledWith("changed", JSON.stringify([]));
    expect(mockCore.setOutput).toHaveBeenCalledWith("count", 0);
    expect(mockCore.setOutput).toHaveBeenCalledWith("count-added", 0);
    expect(mockCore.setOutput).toHaveBeenCalledWith("count-modified", 0);
    expect(mockCore.setOutput).toHaveBeenCalledWith("count-deleted", 0);
  });
});
