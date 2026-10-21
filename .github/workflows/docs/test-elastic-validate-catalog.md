# test-elastic-validate-catalog

Test workflow for `elastic-validate-catalog`. Run the catalog-info validation

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-elastic-validate-catalog.yml`](../test-elastic-validate-catalog.yml#L1-L50) |
| Trigger | `merge_group`; `workflow_dispatch`; `pull_request` (paths: `elastic/validate-catalog/**, .github/workflows/test-elastic-validate-catalog.yml`); `push` (branches: `main`; paths: `elastic/validate-catalog/**, .github/workflows/test-elastic-validate-catalog.yml`) |

## Purpose

Test workflow for `elastic-validate-catalog`. Run the catalog-info validation

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `pull_request` (paths: `elastic/validate-catalog/**, .github/workflows/test-elastic-validate-catalog.yml`); `push` (branches: `main`; paths: `elastic/validate-catalog/**, .github/workflows/test-elastic-validate-catalog.yml`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-slim` | main, failed | `Default GitHub condition` | `—` |
| `main` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `failed` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | check | `elastic/oblt-actions/check-dependent-jobs@v1` | `—` | `jobs` |
| 2 | Step 2 | `${{ steps.check.outputs.is-success }}` | `—` | — |

### `main` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `touch catalog-info.yaml` | `—` | — |
| 3 | Step 3 | `./elastic/validate-catalog` | `—` | — |

### `failed` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `echo "wrong-content" > catalog-info.yaml` | `—` | — |
| 3 | validate-catalog | `./elastic/validate-catalog` | `—` | — |
| 4 | Assert is failure | `test "${{steps.validate-catalog.outcome}}" = "failure"` | `—` | — |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read, packages: read`; job overrides: `none`. |
| Local actions | [`elastic/validate-catalog/action.yml`](../../../elastic/validate-catalog/action.yml); [usage README](../../../elastic/validate-catalog/README.md) — Run the catalog-info validation Inputs: `container-image`, `github-token`. Declared outputs: none declared. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `is-success`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | No `secrets.*` references found in the workflow source. |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-elastic-validate-catalog.yml`](../test-elastic-validate-catalog.yml#L1-50)
- Local action: [`elastic/validate-catalog/action.yml`](../../../elastic/validate-catalog/action.yml) and [`elastic/validate-catalog/README.md`](../../../elastic/validate-catalog/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
