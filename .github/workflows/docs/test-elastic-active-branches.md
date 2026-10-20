# test-elastic-active-branches

Test workflow for `elastic-active-branches`. Fetch the current list of active branches in Elastic (the ones based on the Unified Release process)

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-elastic-active-branches.yml`](../test-elastic-active-branches.yml#L1-L85) |
| Trigger | `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/test-elastic-active-branches.yml, elastic/active-branches/**`); `push` (branches: `main`; paths: `.github/workflows/test-elastic-active-branches.yml, elastic/active-branches/**`) |

## Purpose

Test workflow for `elastic-active-branches`. Fetch the current list of active branches in Elastic (the ones based on the Unified Release process)

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/test-elastic-active-branches.yml, elastic/active-branches/**`); `push` (branches: `main`; paths: `.github/workflows/test-elastic-active-branches.yml, elastic/active-branches/**`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-slim` | main, exclude-main, filter, ubuntu-latest | `Default GitHub condition` | `—` |
| `ubuntu-latest` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `main` | `ubuntu-slim` | None declared | `Default GitHub condition` | `—` |
| `exclude-main` | `ubuntu-slim` | None declared | `Default GitHub condition` | `—` |
| `filter` | `ubuntu-slim` | None declared | `Default GitHub condition` | `—` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | check | `elastic/oblt-actions/check-dependent-jobs@v1` | `—` | `jobs` |
| 2 | Step 2 | `${{ steps.check.outputs.is-success }}` | `—` | — |

### `ubuntu-latest` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | active-branches | `./elastic/active-branches` | `—` | — |
| 3 | Verify main is in the active branches | `echo "Main branch could not be found" && exit 1` | `${{ !contains(fromJSON(steps.active-branches.outputs.branches), 'main') }}` | — |

### `main` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | active-branches | `./elastic/active-branches` | `—` | — |
| 3 | Verify main is in the active branches | `echo "Main branch could not be found" && exit 1` | `${{ !contains(fromJSON(steps.active-branches.outputs.branches), 'main') }}` | — |

### `exclude-main` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | active-branches | `./elastic/active-branches` | `—` | `exclude-branches` |
| 3 | Verify main is not in the active branches | `echo "Main branch could be found but should be excluded" && exit 1` | `contains(fromJSON(steps.active-branches.outputs.branches), 'main')` | — |

### `filter` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | active-branches | `./elastic/active-branches` | `—` | `filter-branches` |
| 3 | Verify main is in the active branches | `echo "Main branch could not be found" && exit 1` | `${{ !contains(fromJSON(steps.active-branches.outputs.branches), 'main') }}` | — |
| 4 | Verify 8.x is not in the active branches | `echo "Main branch could not be found" && exit 1` | `${{ contains(fromJSON(steps.active-branches.outputs.branches), '8.x') }}` | — |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read`; job overrides: `filter: contents: read`. |
| Local actions | [`elastic/active-branches/action.yml`](../../../elastic/active-branches/action.yml); [usage README](../../../elastic/active-branches/README.md) — Fetch the current list of active branches in Elastic (the ones based on the Unified Release process) Inputs: `exclude-branches`, `filter-branches`, `github-token`, `github-repository`. Declared outputs: `matrix`, `branches`. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `is-success`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | No `secrets.*` references found in the workflow source. |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-elastic-active-branches.yml`](../test-elastic-active-branches.yml#L1-85)
- Local action: [`elastic/active-branches/action.yml`](../../../elastic/active-branches/action.yml) and [`elastic/active-branches/README.md`](../../../elastic/active-branches/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
