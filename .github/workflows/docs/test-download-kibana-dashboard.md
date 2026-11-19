# test-download-kibana-dashboard

Test workflow for `download-kibana-dashboard`. An Action to download a Kibana dashboard in png.

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-download-kibana-dashboard.yml`](../test-download-kibana-dashboard.yml#L1-L59) |
| Trigger | `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/test-download-kibana-dashboard.yml, download-kibana-dashboard/**`); `push` (branches: `main`; paths: `.github/workflows/test-download-kibana-dashboard.yml, download-kibana-dashboard/**`) |

## Purpose

Test workflow for `download-kibana-dashboard`. An Action to download a Kibana dashboard in png.

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/test-download-kibana-dashboard.yml, download-kibana-dashboard/**`); `push` (branches: `main`; paths: `.github/workflows/test-download-kibana-dashboard.yml, download-kibana-dashboard/**`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `elastic/oblt-actions/google/auth@v1` | `${{ github.event_name != 'merge_group' }}` | — |
| 2 | Get token | `actions/create-github-app-token@v3` | `${{ github.event_name != 'merge_group' }}` | `app-id`, `private-key`, `permission-contents`, `repositories` |
| 3 | Step 3 | `elastic/oblt-actions/oblt-cli/cluster-credentials@v1` | `${{ github.event_name != 'merge_group' }}` | `github-token`, `cluster-name` |
| 4 | Step 4 | `actions/checkout@v7` | `—` | — |
| 5 | Step 5 | `./download-kibana-dashboard` | `${{ github.event_name != 'merge_group' }}` | `kibana-host`, `kibana-user`, `kibana-password`, `dashboard-id` |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read`; job overrides: `test: contents: read, id-token: write`. |
| Local actions | [`download-kibana-dashboard/action.yml`](../../../download-kibana-dashboard/action.yml); [usage README](../../../download-kibana-dashboard/README.md) — An Action to download a Kibana dashboard in png. Inputs: `kibana-host`, `kibana-user`, `kibana-password`, `dashboard-title`, `dashboard-id`, `from-date`, `to-date`, `png-filename`, `table-width`, `if-no-files-found`, `max-retries`, `query`. Declared outputs: none declared. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `token`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | `OBS_AUTOMATION_APP_ID`, `OBS_AUTOMATION_APP_PEM` |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-download-kibana-dashboard.yml`](../test-download-kibana-dashboard.yml#L1-59)
- Local action: [`download-kibana-dashboard/action.yml`](../../../download-kibana-dashboard/action.yml) and [`download-kibana-dashboard/README.md`](../../../download-kibana-dashboard/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
