# test-oblt-cli-cluster-name-validation

Test workflow for `oblt-cli-cluster-name-validation`. Get the cluster name based on the parameters

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-oblt-cli-cluster-name-validation.yml`](../test-oblt-cli-cluster-name-validation.yml#L1-L103) |
| Trigger | `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/test-oblt-cli-cluster-name-validation.yml, oblt-cli/cluster-name-validation/**`); `push` (branches: `main`; paths: `.github/workflows/test-oblt-cli-cluster-name-validation.yml, oblt-cli/cluster-name-validation/**`) |

## Purpose

Test workflow for `oblt-cli-cluster-name-validation`. Get the cluster name based on the parameters

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/test-oblt-cli-cluster-name-validation.yml, oblt-cli/cluster-name-validation/**`); `push` (branches: `main`; paths: `.github/workflows/test-oblt-cli-cluster-name-validation.yml, oblt-cli/cluster-name-validation/**`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-slim` | cluster-name, cluster-info-file, failures | `always()` | `—` |
| `cluster-name` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `failures` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `cluster-info-file` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | check | `elastic/oblt-actions/check-dependent-jobs@v1` | `—` | `jobs` |
| 2 | Step 2 | `${{ steps.check.outputs.is-success }}` | `—` | — |

### `cluster-name` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | validation | `./oblt-cli/cluster-name-validation` | `—` | `cluster-name` |
| 3 | Assert is foo | `test "${{steps.validation.outputs.cluster-name}}" = "foo"` | `—` | — |

### `failures` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | validation | `./.github/actions/oblt-cli-cluster-name-validation` | `—` | `cluster-name` |
| 3 | Assert is failure | `test "${{steps.validation.outcome}}" = "failure"` | `—` | — |
| 4 | validation1 | `./.github/actions/oblt-cli-cluster-name-validation` | `—` | `cluster-info-file` |
| 5 | Assert is failure | `test "${{steps.validation1.outcome}}" = "failure"` | `—` | — |
| 6 | validation2 | `./.github/actions/oblt-cli-cluster-name-validation` | `—` | `cluster-info-file`, `cluster-name` |
| 7 | Assert is failure | `test "${{steps.validation2.outcome}}" = "failure"` | `—` | — |
| 8 | Step 8 | `echo "{\"ClusterName\":\"bar\"}" \| tee ${{ github.workspace }}/cluster-info.json` | `—` | — |
| 9 | validation3 | `./.github/actions/oblt-cli-cluster-name-validation` | `—` | `cluster-info-file`, `cluster-name` |
| 10 | Assert is failure | `test "${{steps.validation3.outcome}}" = "failure"` | `—` | — |

### `cluster-info-file` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `echo "{\"ClusterName\":\"bar\"}" \| tee ${{ github.workspace }}/cluster-info.json` | `—` | — |
| 3 | validation | `./oblt-cli/cluster-name-validation` | `—` | `cluster-info-file` |
| 4 | Assert is bar | `test "${{steps.validation.outputs.cluster-name}}" = "bar"` | `—` | — |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read`; job overrides: `none`. |
| Local actions | [`oblt-cli/cluster-name-validation/action.yml`](../../../oblt-cli/cluster-name-validation/action.yml); [usage README](../../../oblt-cli/cluster-name-validation/README.md) — Get the cluster name based on the parameters Inputs: `cluster-name`, `cluster-info-file`. Declared outputs: `cluster-name`.<br>`.github/actions/oblt-cli-cluster-name-validation` is referenced by the workflow but has no checked-in source in this checkout. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `cluster-name, is-success`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | No `secrets.*` references found in the workflow source. |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-oblt-cli-cluster-name-validation.yml`](../test-oblt-cli-cluster-name-validation.yml#L1-103)
- Local action: [`oblt-cli/cluster-name-validation/action.yml`](../../../oblt-cli/cluster-name-validation/action.yml) and [`oblt-cli/cluster-name-validation/README.md`](../../../oblt-cli/cluster-name-validation/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
