# test-github-user-type

Test workflow for `github-user-type`. Get GitHub user type

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-github-user-type.yml`](../test-github-user-type.yml#L1-L98) |
| Trigger | `merge_group`; `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-github-user-type.yml, github/user-type/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-github-user-type.yml, github/user-type/**`) |

## Purpose

Test workflow for `github-user-type`. Get GitHub user type

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-github-user-type.yml, github/user-type/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-github-user-type.yml, github/user-type/**`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-slim` | is-bot, is-not-bot | `always()` | `—` |
| `is-bot` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `copilot-is-bot` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `is-not-bot` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | check | `elastic/oblt-actions/check-dependent-jobs@v1` | `—` | `jobs` |
| 2 | Step 2 | `${{ steps.check.outputs.is-success }}` | `—` | — |

### `is-bot` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `elastic/oblt-actions/git/setup@v1` | `—` | — |
| 3 | Get token | `actions/create-github-app-token@v3` | `—` | `app-id`, `private-key`, `permission-members` |
| 4 | validation | `./github/user-type` | `—` | `github-token`, `github-user` |
| 5 | Assert is bot | `test "${{steps.validation.outputs.result}}" = "bot"` | `—` | — |

### `copilot-is-bot` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `elastic/oblt-actions/git/setup@v1` | `—` | — |
| 3 | Get token | `actions/create-github-app-token@v3` | `—` | `app-id`, `private-key`, `permission-members` |
| 4 | validation | `./github/user-type` | `—` | `github-token`, `github-user` |
| 5 | Assert is bot | `test "${{steps.validation.outputs.result}}" = "bot"` | `—` | — |

### `is-not-bot` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `elastic/oblt-actions/git/setup@v1` | `—` | — |
| 3 | Get token | `actions/create-github-app-token@v3` | `—` | `app-id`, `private-key`, `permission-members` |
| 4 | validation | `./github/user-type` | `—` | `github-token`, `github-user` |
| 5 | Assert is not bot | `test "${{steps.validation.outputs.result}}" = "user"` | `—` | — |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read`; job overrides: `none`. |
| Local actions | [`github/user-type/action.yml`](../../../github/user-type/action.yml); [usage README](../../../github/user-type/README.md) — Get GitHub user type Inputs: `github-token`, `github-user`. Declared outputs: `result`. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `is-success, result, token`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | `OBS_AUTOMATION_APP_ID`, `OBS_AUTOMATION_APP_PEM` |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-github-user-type.yml`](../test-github-user-type.yml#L1-98)
- Local action: [`github/user-type/action.yml`](../../../github/user-type/action.yml) and [`github/user-type/README.md`](../../../github/user-type/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
