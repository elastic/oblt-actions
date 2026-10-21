# test-check-dependent-jobs

Test workflow for `check-dependent-jobs`. Evaluates the combined the status results of the provided needs context.

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-check-dependent-jobs.yml`](../test-check-dependent-jobs.yml#L1-L93) |
| Trigger | `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/test-check-dependent-jobs.yml, check-dependent-jobs/**`); `push` (branches: `main`; paths: `.github/workflows/test-check-dependent-jobs.yml, check-dependent-jobs/**`) |

## Purpose

Test workflow for `check-dependent-jobs`. Evaluates the combined the status results of the provided needs context.

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/test-check-dependent-jobs.yml, check-dependent-jobs/**`); `push` (branches: `main`; paths: `.github/workflows/test-check-dependent-jobs.yml, check-dependent-jobs/**`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-slim` | test-success, test-failure-and-success, test-failures, test-skipped-default, test-skipped-opt-in | `always()` | `—` |
| `test-success` | `ubuntu-slim` | None declared | `Default GitHub condition` | `—` |
| `test-failure-and-success` | `ubuntu-slim` | None declared | `Default GitHub condition` | `—` |
| `test-failures` | `ubuntu-slim` | None declared | `Default GitHub condition` | `—` |
| `test-skipped-default` | `ubuntu-slim` | None declared | `Default GitHub condition` | `—` |
| `test-skipped-opt-in` | `ubuntu-slim` | None declared | `Default GitHub condition` | `—` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | check | `elastic/oblt-actions/check-dependent-jobs@v1` | `—` | `jobs` |
| 2 | Step 2 | `${{ steps.check.outputs.is-success }}` | `—` | — |

### `test-success` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | check | `./check-dependent-jobs` | `—` | `jobs` |
| 3 | assert outputs.is-success==true | `test "${{ steps.check.outputs.is-success }}" = "true"` | `—` | — |

### `test-failure-and-success` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | check-2 | `./check-dependent-jobs` | `—` | `jobs` |
| 3 | assert outputs.is-success==false | `test "${{ steps.check-2.outputs.is-success }}" = "false"` | `—` | — |

### `test-failures` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | check-3 | `./check-dependent-jobs` | `—` | `jobs` |
| 3 | assert outputs.is-success==false | `test "${{ steps.check-3.outputs.is-success }}" = "false"` | `—` | — |

### `test-skipped-default` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | check-4 | `./check-dependent-jobs` | `—` | `jobs` |
| 3 | assert outputs.is-success==false | `test "${{ steps.check-4.outputs.is-success }}" = "false"` | `—` | — |

### `test-skipped-opt-in` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | check-5 | `./check-dependent-jobs` | `—` | `jobs`, `skipped-as-success` |
| 3 | assert outputs.is-success==true | `test "${{ steps.check-5.outputs.is-success }}" = "true"` | `—` | — |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read`; job overrides: `none`. |
| Local actions | [`check-dependent-jobs/action.yml`](../../../check-dependent-jobs/action.yml); [usage README](../../../check-dependent-jobs/README.md) — Evaluates the combined the status results of the provided needs context. Inputs: `jobs`, `skipped-as-success`. Declared outputs: `is-success`, `status`. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `is-success`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | No `secrets.*` references found in the workflow source. |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-check-dependent-jobs.yml`](../test-check-dependent-jobs.yml#L1-93)
- Local action: [`check-dependent-jobs/action.yml`](../../../check-dependent-jobs/action.yml) and [`check-dependent-jobs/README.md`](../../../check-dependent-jobs/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
