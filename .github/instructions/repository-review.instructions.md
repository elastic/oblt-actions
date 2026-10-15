---
applyTo: "**"
---

# Repository review guidance

- For GitHub Action changes, prefer end-to-end evidence in `.github/workflows/test-<action>.yml` or colocated action tests. Exercise composite actions through `uses: ./<action-path>` so the test covers metadata and runtime behavior, not only isolated logic.
- Keep actions single-purpose with clear inputs and outputs; avoid combining unrelated side effects. Keep namespaced actions in their own directories with an `action.yml`.
- When an action's inputs, outputs, or usage change, keep its README examples aligned with the declared contract.
- Keep changes focused and reviewable. For the review workflow, follow `.agents/skills/copilot-review/SKILL.md`; repository-specific checks are in this file and `.github/instructions/github-actions.instructions.md`.

## Domain focus

- For changes under `edot-release/**` or to `.github/edot-release.json`, verify that release tags and full-history inputs, version/range outputs, and preparation/finalization branch handoffs remain consistent; a mismatch can publish the wrong version or omit contributing pull requests.
- For changes to `oblt-cli/deploy-my-kibana`, `oblt-cli/undeploy-my-kibana`, or their workflows, verify the `deploy-custom-kibana` and `destroy-custom-kibana-serverless` issue-label routing stays aligned; mismatched labels can prevent deployment or leave a Kibana environment running after teardown is requested.
- For changes to `aws/auth`, `azure/auth`, or `google/auth`, verify configured account, project, tenant, and derived identity values still target the intended cloud identity; incorrect mapping can authenticate jobs to the wrong account or prevent cloud operations from running.

## Deterministic checks

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
