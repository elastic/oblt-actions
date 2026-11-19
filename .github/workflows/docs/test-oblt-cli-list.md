# test-oblt-cli-list

Test workflow for `oblt-cli-list`. List clusters using a filter

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-oblt-cli-list.yml`](../test-oblt-cli-list.yml#L1-L38) |
| Trigger | `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/test-oblt-cli-list.yml, oblt-cli/list/**`); `push` (branches: `main`; paths: `.github/workflows/test-oblt-cli-list.yml, oblt-cli/list/**`) |

## Purpose

Test workflow for `oblt-cli-list`. List clusters using a filter

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/test-oblt-cli-list.yml, oblt-cli/list/**`); `push` (branches: `main`; paths: `.github/workflows/test-oblt-cli-list.yml, oblt-cli/list/**`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Get token | `actions/create-github-app-token@v3` | `—` | `app-id`, `private-key`, `permission-contents`, `repositories` |
| 3 | Step 3 | `./oblt-cli/list` | `—` | `github-token` |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read`; job overrides: `none`. |
| Local actions | [`oblt-cli/list/action.yml`](../../../oblt-cli/list/action.yml); [usage README](../../../oblt-cli/list/README.md) — List clusters using a filter Inputs: `github-token`, `slack-channel`, `username`, `version`, `verbose`, `filter-key`, `filter-value`, `filter-expiry-date-before-than`, `all`, `fail-on-empty`, `save-to-file`, `version-file`. Declared outputs: none declared. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `token`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | `OBS_AUTOMATION_APP_ID`, `OBS_AUTOMATION_APP_PEM` |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-oblt-cli-list.yml`](../test-oblt-cli-list.yml#L1-38)
- Local action: [`oblt-cli/list/action.yml`](../../../oblt-cli/list/action.yml) and [`oblt-cli/list/README.md`](../../../oblt-cli/list/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
