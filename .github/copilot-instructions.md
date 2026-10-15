<!-- configure-ai-review:baseline:start -->
# High-signal code review policy

These rules apply only when reviewing a pull request. They do not apply to Copilot Chat or cloud agent tasks. When reviewing, default to leaving no comment. Comment only when the changed code introduces a concrete correctness, security, data-integrity, compatibility, reliability, rollout, or operability defect, or when changed material behavior has no test that would catch a regression (see "Missing tests for material behavior" below).

When multiple issues compete for attention, prioritize in this order: (1) concrete correctness, security, or data-integrity defects; (2) architectural or design problems with a concrete, describable consequence; (3) missing test coverage for changed behavior. Leave the highest-priority comments first.

Do not comment on wording, spelling, formatting, naming preferences, syntax, style, import ordering, or other concerns that a compiler, formatter, linter, schema validator, test, or CI check enabled in this repository already reports. Do not restate a failing automated check. Do not leave praise, summaries, optional refactors, generic best practices, or speculative suggestions.

Before leaving a comment, verify all of the following:

- The issue is introduced or made materially worse by this pull request.
- You can describe a specific failure scenario and its impact.
- The finding starts from the changed lines. You may read callers, tests, and configuration to confirm it, but do not report issues the diff does not introduce or make worse.
- The repository's current code and configuration support the claim.
- The comment identifies the affected path and gives an actionable correction or asks for concrete missing evidence.
- The expected value of the comment is high enough to interrupt a human reviewer.

If any condition is missing, remain silent. Express uncertainty only when the uncertainty itself is a material risk that the author can resolve with specific evidence. On a re-review after new commits, do not repeat a comment on a line that has not changed since the prior run.

Use the repository's `.github/skills/code-review/SKILL.md` for domain-specific review checks when it exists. Copilot review is advisory. Whether its approval counts toward required approvals is controlled by org and branch settings, not this file.

## Trust-boundary and supply-chain changes

Always inspect a diff that changes CI, build, release, dependency, credential,
network, or security configuration. Note: Copilot code review does not inspect
lockfiles, `requirements.txt`, or generated files — leave those to Dependabot
and human review. Leave a review comment when the change introduces or materially
broadens a capability without a concrete, repository-supported need and an
appropriate control. In particular, flag:

- broader token, role, cloud, repository, or secret permissions than the changed
  operation requires;
- new collection, copying, logging, caching, artifact upload, or persistence of
  credentials or secret-bearing worker state;
- privileged workflows that check out, download, or execute untrusted pull-
  request code, artifacts, build scripts, hooks, or dependency lifecycle scripts;
- new outbound destinations, telemetry, uploads, remote shells, or network
  services unrelated to the repository's documented responsibility;
- downloaded or remotely referenced code, actions, reusable workflows, images,
  plugins, tools, or binaries that are executed without immutable identity and
  integrity verification;
- new dependencies or build inputs that are not resolved immutably;
- weakened or bypassed tests, approval gates, secret scanning, signature or
  checksum verification, TLS verification, sandboxing, or least-privilege
  defaults;
- shared caches, workspaces, or non-ephemeral runners that allow an untrusted or
  earlier build to influence a privileged or later build;
- unexplained executable binaries, encoded or obfuscated payloads, generated
  code without a documented generator, or functionality unrelated to the
  repository's stated purpose;
- untrusted input, such as a pull-request title, branch name, or issue body,
  placed directly into a `run:` script through a `${{ }}` expression instead
  of through an environment variable.

For GitHub Actions, require third-party actions and reusable workflows to be
pinned to a full commit SHA from the intended upstream repository. Require
container images by digest when they execute in CI, build, release, or
production paths. Require downloaded executables or scripts to be pinned to an
immutable version and verified before execution with an expected cryptographic
digest, or with a signature or attestation from an expected signer. HTTPS or a
checksum downloaded from the same mutable source is not sufficient integrity
evidence. Reject pipe-to-shell execution of unverified remote content.

For package-manager dependencies, require the repository's lockfile or equivalent
immutable resolution to be committed and enforced. Do not comment on a version
range merely because it is a range when an enforced lockfile pins the resolved
artifact. Do comment when a new executable build or runtime dependency can float
without reviewed immutable resolution.

Describe the exact new trust path, the realistic abuse or compromise scenario,
and the smallest corrective control. Do not allege malicious intent; when code
appears unrelated or concealed, ask for concrete purpose and provenance and
recommend removal when neither is established.

## Missing tests for material behavior

Check whether changed behavior has meaningful deterministic coverage. Comment
when the diff adds or changes a material correctness, security, compatibility,
failure-handling, state-transition, permission, parsing, retry, concurrency,
build, or release behavior and no existing or new test would fail if that
behavior regressed. A bug fix should normally include a regression test that
fails for the original defect.

Before commenting, inspect the relevant existing tests, including higher-level
and generated-output tests. Do not request tests for documentation-only changes,
mechanical refactors with unchanged behavior, generated files whose source and
generation are already tested, or behavior already exercised at an appropriate
layer. Do not demand a unit test when an existing integration or end-to-end test
more directly covers the contract.

A missing-test comment must name the unverified behavior and a concrete scenario
and assertion that would catch a realistic regression. Do not leave a generic
"add tests" comment or prescribe test-file structure. When deterministic testing
is genuinely impractical, ask for specific reproducible verification evidence
and the reason it cannot be automated.
<!-- configure-ai-review:baseline:end -->
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

## Repository review specifics

### Language and toolchain

The repository provides GitHub composite actions declared in `action.yml`, implemented mainly in Bash, Python, and Node.js; action-local `.node-version` files pin Node.js where present, while `package.json` files declare package scripts and dependencies. There is no repository-wide language version pin.

### Domain focus

- For changes under `edot-release/**` or to `.github/edot-release.json`, verify that release tags and full-history inputs, version/range outputs, and preparation/finalization branch handoffs remain consistent; a mismatch can publish the wrong version or omit contributing pull requests.
- For changes to `oblt-cli/deploy-my-kibana`, `oblt-cli/undeploy-my-kibana`, or their workflows, verify the `deploy-custom-kibana` and `destroy-custom-kibana-serverless` issue-label routing stays aligned; mismatched labels can prevent deployment or leave a Kibana environment running after teardown is requested.
- For changes to `aws/auth`, `azure/auth`, or `google/auth`, verify configured account, project, tenant, and derived identity values still target the intended cloud identity; incorrect mapping can authenticate jobs to the wrong account or prevent cloud operations from running.

### Deterministic checks

CI runs the root `.pre-commit-config.yaml` through `.github/workflows/pre-commit.yml`; do not duplicate these checks:

- `actionlint` checks GitHub Actions workflow syntax, structure, and expressions.
- `gh-action-readme/action-readme` checks action README metadata and generated usage documentation.
- `check-merge-conflict` detects conflict markers.
- `check-yaml` validates YAML syntax.
- `check-xml` validates XML syntax.
- `end-of-file-fixer` enforces final newlines.
- Jest runs the JavaScript action tests in the changed-files and mutex workflows.
- `mixed-line-ending` enforces consistent line endings.
- `trailing-whitespace` detects trailing whitespace.
- Dependabot manages dependency update pull requests; do not comment on dependency version ranges it updates.
