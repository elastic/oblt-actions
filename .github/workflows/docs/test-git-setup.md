# test-git-setup

Test workflow for `git-setup`. Setup the git usename, email, and authentication with git CLI. After this action you can use https URL repos in git commands. The GITHUB_TOKEN (not needed here) will be used to authenticate with the git CLI, after this action.

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-git-setup.yml`](../test-git-setup.yml#L1-L58) |
| Trigger | `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/test-git-setup.yml, git/setup/**`); `push` (branches: `main`; paths: `.github/workflows/test-git-setup.yml, git/setup/**`) |

## Purpose

Test workflow for `git-setup`. Setup the git usename, email, and authentication with git CLI. After this action you can use https URL repos in git commands. The GITHUB_TOKEN (not needed here) will be used to authenticate with the git CLI, after this action.

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/test-git-setup.yml, git/setup/**`); `push` (branches: `main`; paths: `.github/workflows/test-git-setup.yml, git/setup/**`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-slim` | None declared | `Default GitHub condition` | `—` |
| `test-newline-injection` | `ubuntu-slim` | None declared | `Default GitHub condition` | `—` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `./git/setup` | `—` | — |
| 3 | validate git user | `test "$(git config user.name)" = "obltmachine"` | `—` | — |
| 4 | validate git email | `test "$(git config user.email)" = "obltmachine@users.noreply.github.com"` | `—` | — |
| 5 | validate GIT_USER env | `test "${GIT_USER}" = "obltmachine"` | `—` | — |
| 6 | validate GIT_EMAIL env | `test "${GIT_EMAIL}" = "obltmachine@users.noreply.github.com"` | `—` | — |

### `test-newline-injection` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `./git/setup` | `—` | `username`, `email` |
| 3 | assert no env var injection via username | `if [ -n "${INJECTED_VAR}" ]; then echo "FAIL: INJECTED_VAR was set, newline injection succeeded" exit 1 fi echo "PASS: INJECTED_VAR is not set"` | `—` | — |
| 4 | assert no env var injection via email | `if [ -n "${INJECTED_EMAIL_VAR}" ]; then echo "FAIL: INJECTED_EMAIL_VAR was set, newline injection succeeded" exit 1 fi echo "PASS: INJECTED_EMAIL_VAR is not set"` | `—` | — |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read`; job overrides: `none`. |
| Local actions | [`git/setup/action.yml`](../../../git/setup/action.yml); [usage README](../../../git/setup/README.md) — Setup the git usename, email, and authentication with git CLI. After this action you can use https URL repos in git commands. The GITHUB_TOKEN (not needed here) will be used to authenticate with the git CLI, after this action. Inputs: `username`, `email`, `trace`, `github-token`. Declared outputs: none declared. |
| Outputs | No workflow/job outputs are declared. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | No `secrets.*` references found in the workflow source. |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-git-setup.yml`](../test-git-setup.yml#L1-58)
- Local action: [`git/setup/action.yml`](../../../git/setup/action.yml) and [`git/setup/README.md`](../../../git/setup/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
