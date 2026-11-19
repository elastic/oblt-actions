# test-mergify-labels-copier

Test workflow for `mergify-labels-copier`. copies pull request labels to backported PRs

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-mergify-labels-copier.yml`](../test-mergify-labels-copier.yml#L1-L45) |
| Trigger | `merge_group`; `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-mergify-labels-copier.yml, mergify/labels-copier/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-mergify-labels-copier.yml, mergify/labels-copier/**`) |

## Purpose

Test workflow for `mergify-labels-copier`. copies pull request labels to backported PRs

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-mergify-labels-copier.yml, mergify/labels-copier/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-mergify-labels-copier.yml, mergify/labels-copier/**`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Get token | `actions/create-github-app-token@v3` | `—` | `app-id`, `private-key`, `permission-pull-requests` |
| 3 | validation | `./mergify/labels-copier` | `—` | `github-token`, `repository`, `pull-request`, `excluded-labels-regex`; `DRY_RUN` |
| 4 | assert labels are not empty | `test -n "${{ steps.validation.outputs.labels }}"` | `—` | — |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read`; job overrides: `none`. |
| Local actions | [`mergify/labels-copier/action.yml`](../../../mergify/labels-copier/action.yml); [usage README](../../../mergify/labels-copier/README.md) — copies pull request labels to backported PRs Inputs: `excluded-labels-regex`, `github-token`, `repository`, `pull-request`. Declared outputs: `labels`. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `labels, token`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | `OBS_AUTOMATION_APP_ID`, `OBS_AUTOMATION_APP_PEM` |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-mergify-labels-copier.yml`](../test-mergify-labels-copier.yml#L1-45)
- Local action: [`mergify/labels-copier/action.yml`](../../../mergify/labels-copier/action.yml) and [`mergify/labels-copier/README.md`](../../../mergify/labels-copier/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
