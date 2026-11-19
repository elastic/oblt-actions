# test-pre-commit

Test workflow for `pre-commit`. Run pre-commit independently you are running on a PR or a branch.

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-pre-commit.yml`](../test-pre-commit.yml#L1-L61) |
| Trigger | `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/test-pre-commit.yml, pre-commit/**`); `push` (branches: `main`; paths: `.github/workflows/test-pre-commit.yml, pre-commit/**`) |

## Purpose

Test workflow for `pre-commit`. Run pre-commit independently you are running on a PR or a branch.

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/test-pre-commit.yml, pre-commit/**`); `push` (branches: `main`; paths: `.github/workflows/test-pre-commit.yml, pre-commit/**`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-slim` | default, version | `Default GitHub condition` | `—` |
| `default` | `ubuntu-slim` | None declared | `Default GitHub condition` | `—` |
| `version` | `ubuntu-slim` | None declared | `Default GitHub condition` | `—` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | check | `elastic/oblt-actions/check-dependent-jobs@v1` | `—` | `jobs` |
| 2 | Step 2 | `${{ steps.check.outputs.is-success }}` | `—` | — |

### `default` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `./pre-commit` | `—` | — |
| 3 | Verify python version | `got=$(python --version 2>&1) echo "${got} == ${want}" [[ "${got}" == *"${want}"* ]]` | `—` | — |

### `version` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `./pre-commit` | `—` | `python-version` |
| 3 | Verify python version | `got=$(python --version 2>&1) echo "${got} == ${want}" [[ "${got}" == *"${want}"* ]]` | `—` | — |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read`; job overrides: `none`. |
| Local actions | [`pre-commit/action.yml`](../../../pre-commit/action.yml); [usage README](../../../pre-commit/README.md) — Run pre-commit independently you are running on a PR or a branch. Inputs: `clean-checkout`, `python-version`. Declared outputs: none declared. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `is-success`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | No `secrets.*` references found in the workflow source. |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-pre-commit.yml`](../test-pre-commit.yml#L1-61)
- Local action: [`pre-commit/action.yml`](../../../pre-commit/action.yml) and [`pre-commit/README.md`](../../../pre-commit/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
