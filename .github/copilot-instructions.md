# AI agent instructions for oblt-actions

This file provides guidance to AI agents (Claude Code, GitHub Copilot, etc.) when working with code in this repository.

## Meta instructions

Important: Keep this file accurate and up to date. Update it immediately when (1) users give new instructions, (2) you find contradictions, or (3) new patterns or standards emerge. Treat this maintenance as a blocking, highest‑priority task that doesn’t need an explicit prompt.

Note: This file is exempt from the “no new docs” rule below. Proactively edit and maintain this file as part of your duties.

## Repository-specific review guidance for Copilot code review

When reviewing pull requests in this repository, prioritize the following:

- Validate end-to-end behavior before approving. For GitHub Action changes, prefer evidence of real behavior through dedicated workflows in `.github/workflows/test-<action>.yml` or colocated action tests. For composite actions, end-to-end validation should exercise the action via `uses: ./<action-path>` rather than relying only on isolated unit logic.
- Keep actions simple and focused. Each action should do one job, expose clear inputs and outputs, and avoid mixing unrelated concerns or side effects in the same action or workflow. Keep the repository layout simple: top-level folders are individual GitHub composite actions, and namespaced actions stay in dedicated subdirectories with their own `action.yml`.
- Apply GitHub hardening principles consistently. Use explicit least-privilege `permissions`, avoid broad `write-all` or unscoped tokens, do not log or expose secrets, validate untrusted input before passing it to shell commands, and prefer explicit token scoping and OIDC where appropriate.
- Prefer small, reviewable edits. Avoid unrelated refactors or scope creep. If a change does not include the required test coverage or does not align with the repository's action structure, call it out in review feedback.
- Maintain documentation and metadata discipline. When action inputs, outputs, or usage change, update the action's `README.md` and keep examples consistent with the declared contract.

Review feedback should call out missing e2e coverage, missing security hardening, or mixed concerns before raising low-signal style issues.

## Code Standards

### Required before each commit

- run precommit hooks before committing.

### Development flow

- Create a feature branch from `main` for each task.
- Write code, tests, and documentation as needed.
- Create a test GitHub action workflow to validate changes.
- The test GitHub action workflow should validate that:
  - All tests pass. Use the existing test workflows (`.github/workflows/test-*`) and colocated action tests (for example `*.test.js`, `*_tests.py`, `test_*.py`) as a guide.
  - Name of the file should be the name of the github action and starts with `test-` and ends with `.yml`.
- Open a pull request against `main` with a clear description of changes.
- Ensure all checks pass before merging.
- Squash and merge pull requests to keep history clean.
- Delete feature branches after merging.
- Update this file as needed to reflect changes in standards or practices.

### Repository structure

- top level folder as individual github composite actions.
- if a folder contains multiple actions, each action should be in its own subfolder with its own `action.yml`.

## Development notes

### Code style

- Follow existing code style and conventions.
- Use consistent indentation and spacing.
- Use meaningful variable and function names.
- Pre-commit hooks enforce code quality.
- Avoid breaking changes to existing functionality unless necessary.
- Write clear, concise, and maintainable code.
- Add comments and documentation where needed.
- Follow best practices for the specific programming language or framework.
- Keep it simple and avoid over-engineering.

### Pull Request

- Tag the PR with relevant labels (e.g., `changelog:breaking`, `changelog:feature`, `changelog:fix`, `changelog:docs`, `changelog:dependencies`, `changelog:ci`).

### Breaking changes

- Clearly document breaking changes in the pull request description.
- Use the `changelog:breaking` label for pull requests that introduce breaking changes.
- Update any relevant documentation to reflect breaking changes.
- Update the description of https://github.com/elastic/oblt-actions/issues/126 to reflect the breaking change entry.
- Communicate breaking changes to the team if necessary.

## File creation guidelines

Important: File creation policy
- Do only what the task asks. Don’t add extras.
- Don’t create files unless they’re necessary to achieve the goal.
- Always prefer editing an existing file to creating a new one.
- Exception: Proactively maintain this `.github/copilot-instructions.md` file (see “Meta instructions”).

## Security guidelines

Important: Security policy
- Assist with defensive security tasks only.
- Refuse to create, modify, or improve code that could be used maliciously.
- Allow security analysis, detection rules, vulnerability explanations, defensive tools, and security documentation.
- Always follow security best practices.
- Don’t introduce code that exposes or logs secrets or keys.
- Don’t commit secrets or keys to the repository.
