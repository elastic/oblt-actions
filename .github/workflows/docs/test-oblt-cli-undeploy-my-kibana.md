# test-undeploy-my-kibana

Test workflow for `oblt-cli-undeploy-my-kibana`. Undeploy my kibana given the Pull Request

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-oblt-cli-undeploy-my-kibana.yml`](../test-oblt-cli-undeploy-my-kibana.yml#L1-L72) |
| Trigger | `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/test-undeploy-my-kibana.yml, oblt-cli/undeploy-my-kibana/**`); `push` (branches: `main`; paths: `.github/workflows/test-undeploy-my-kibana.yml, oblt-cli/undeploy-my-kibana/**`) |

## Purpose

Test workflow for `oblt-cli-undeploy-my-kibana`. Undeploy my kibana given the Pull Request

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/test-undeploy-my-kibana.yml, oblt-cli/undeploy-my-kibana/**`); `push` (branches: `main`; paths: `.github/workflows/test-undeploy-my-kibana.yml, oblt-cli/undeploy-my-kibana/**`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `undeploy-my-kibana` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `no-parameters` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `all-parameters` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `test` | `ubuntu-slim` | undeploy-my-kibana, no-parameters, all-parameters | `always()` | `—` |

### `undeploy-my-kibana` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `./oblt-cli/undeploy-my-kibana` | `${{ github.event_name != 'merge_group' }}` | `github-app-id`, `github-app-private-key`, `pull-request`, `repository` |

### `no-parameters` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | validation | `./oblt-cli/undeploy-my-kibana` | `—` | — |
| 3 | Assert is failure if no parameters | `test "${{steps.validation.outcome}}" = "failure"` | `—` | — |

### `all-parameters` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | validation | `./oblt-cli/undeploy-my-kibana` | `—` | `github-app-id`, `github-app-private-key`, `github-token` |
| 3 | Assert is failure if all parameters | `test "${{steps.validation.outcome}}" = "failure"` | `—` | — |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | check | `elastic/oblt-actions/check-dependent-jobs@v1` | `—` | `jobs` |
| 2 | Step 2 | `${{ steps.check.outputs.is-success }}` | `—` | — |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read`; job overrides: `none`. |
| Local actions | [`oblt-cli/undeploy-my-kibana/action.yml`](../../../oblt-cli/undeploy-my-kibana/action.yml); [usage README](../../../oblt-cli/undeploy-my-kibana/README.md) — Undeploy my kibana given the Pull Request Inputs: `pull-request`, `repository`, `github-token`, `github-app-id`, `github-app-private-key`. Declared outputs: `issue`. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `is-success`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | `OBS_AUTOMATION_APP_ID`, `OBS_AUTOMATION_APP_PEM` |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-oblt-cli-undeploy-my-kibana.yml`](../test-oblt-cli-undeploy-my-kibana.yml#L1-72)
- Local action: [`oblt-cli/undeploy-my-kibana/action.yml`](../../../oblt-cli/undeploy-my-kibana/action.yml) and [`oblt-cli/undeploy-my-kibana/README.md`](../../../oblt-cli/undeploy-my-kibana/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
