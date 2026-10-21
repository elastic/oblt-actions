# test-deploy-my-kibana

Test workflow for `oblt-cli-deploy-my-kibana`. Run the deploy my Kibana PR.

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-oblt-cli-deploy-my-kibana.yml`](../test-oblt-cli-deploy-my-kibana.yml#L1-L73) |
| Trigger | `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/test-oblt-cli-deploy-my-kibana.yml, oblt-cli/deploy-my-kibana/**`) |

## Purpose

Test workflow for `oblt-cli-deploy-my-kibana`. Run the deploy my Kibana PR.

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/test-oblt-cli-deploy-my-kibana.yml, oblt-cli/deploy-my-kibana/**`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `deploy-my-kibana` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `no-parameters` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `all-parameters` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `test` | `ubuntu-slim` | deploy-my-kibana, no-parameters, all-parameters | `always()` | `—` |

### `deploy-my-kibana` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `./oblt-cli/deploy-my-kibana` | `${{ github.event_name != 'merge_group' }}` | `github-app-id`, `github-app-private-key`, `comment-url`, `comment-id`, `issue-url`, `repository` |

### `no-parameters` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | validation | `./oblt-cli/deploy-my-kibana` | `${{ github.event_name != 'merge_group' }}` | — |
| 3 | Assert is failure if no parameters | `test "${{steps.validation.outcome}}" = "failure"` | `${{ github.event_name != 'merge_group' }}` | — |

### `all-parameters` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | validation | `./oblt-cli/deploy-my-kibana` | `${{ github.event_name != 'merge_group' }}` | `github-app-id`, `github-app-private-key`, `github-token` |
| 3 | Assert is failure if all parameters | `test "${{steps.validation.outcome}}" = "failure"` | `${{ github.event_name != 'merge_group' }}` | — |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | check | `elastic/oblt-actions/check-dependent-jobs@v1` | `—` | `jobs` |
| 2 | Step 2 | `${{ steps.check.outputs.is-success }}` | `—` | — |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read, pull-requests: write`; job overrides: `none`. |
| Local actions | [`oblt-cli/deploy-my-kibana/action.yml`](../../../oblt-cli/deploy-my-kibana/action.yml); [usage README](../../../oblt-cli/deploy-my-kibana/README.md) — Run the deploy my Kibana PR. Inputs: `comment-url`, `comment-id`, `issue-url`, `repository`, `user`, `github-token`, `github-app-id`, `github-app-private-key`. Declared outputs: `issue`. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `is-success`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | `OBS_AUTOMATION_APP_ID`, `OBS_AUTOMATION_APP_PEM` |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-oblt-cli-deploy-my-kibana.yml`](../test-oblt-cli-deploy-my-kibana.yml#L1-73)
- Local action: [`oblt-cli/deploy-my-kibana/action.yml`](../../../oblt-cli/deploy-my-kibana/action.yml) and [`oblt-cli/deploy-my-kibana/README.md`](../../../oblt-cli/deploy-my-kibana/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
