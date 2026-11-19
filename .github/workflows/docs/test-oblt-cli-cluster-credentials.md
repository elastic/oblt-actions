# test-oblt-cli-cluster-credentials

Test workflow for `oblt-cli-cluster-credentials`. Run the oblt-cli wrapper to retrieve the credentials to connect to the given cluster

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-oblt-cli-cluster-credentials.yml`](../test-oblt-cli-cluster-credentials.yml#L1-L42) |
| Trigger | `merge_group`; `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-oblt-cli-cluster-credentials.yml, oblt-cli/cluster-credentials/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-oblt-cli-cluster-credentials.yml, oblt-cli/cluster-credentials/**`) |

## Purpose

Test workflow for `oblt-cli-cluster-credentials`. Run the oblt-cli wrapper to retrieve the credentials to connect to the given cluster

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-oblt-cli-cluster-credentials.yml, oblt-cli/cluster-credentials/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-oblt-cli-cluster-credentials.yml, oblt-cli/cluster-credentials/**`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `elastic/oblt-actions/google/auth@v1` | `—` | — |
| 3 | Get token | `actions/create-github-app-token@v3` | `—` | `app-id`, `private-key`, `permission-contents`, `repositories` |
| 4 | Step 4 | `./oblt-cli/cluster-credentials` | `—` | `github-token`, `cluster-name` |
| 5 | Step 5 | `curl -X GET "${ELASTICSEARCH_HOST}/_cat/indices?v" -u "${ELASTICSEARCH_USERNAME}:${ELASTICSEARCH_PASSWORD}"` | `—` | — |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read, id-token: write`; job overrides: `none`. |
| Local actions | [`oblt-cli/cluster-credentials/action.yml`](../../../oblt-cli/cluster-credentials/action.yml); [usage README](../../../oblt-cli/cluster-credentials/README.md) — Run the oblt-cli wrapper to retrieve the credentials to connect to the given cluster Inputs: `cluster-name`, `cluster-info-file`, `github-token`. Declared outputs: none declared. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `token`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | `OBS_AUTOMATION_APP_ID`, `OBS_AUTOMATION_APP_PEM` |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-oblt-cli-cluster-credentials.yml`](../test-oblt-cli-cluster-credentials.yml#L1-42)
- Local action: [`oblt-cli/cluster-credentials/action.yml`](../../../oblt-cli/cluster-credentials/action.yml) and [`oblt-cli/cluster-credentials/README.md`](../../../oblt-cli/cluster-credentials/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
