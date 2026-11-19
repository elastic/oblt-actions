# test-updatecli-run

Test workflow for `updatecli-run`. This is an opinionated GitHub Action to run the updatecli

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-updatecli-run.yml`](../test-updatecli-run.yml#L1-L102) |
| Trigger | `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/test-updatecli-run.yml, updatecli/run/**`); `push` (branches: `main`; paths: `.github/workflows/test-updatecli-run.yml, updatecli/run/**`) |

## Purpose

Test workflow for `updatecli-run`. This is an opinionated GitHub Action to run the updatecli

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/test-updatecli-run.yml, updatecli/run/**`); `push` (branches: `main`; paths: `.github/workflows/test-updatecli-run.yml, updatecli/run/**`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-slim` | default, version, version-file, version-file-updatecli | `Default GitHub condition` | `—` |
| `default` | `ubuntu-slim` | None declared | `Default GitHub condition` | `—` |
| `version` | `ubuntu-slim` | None declared | `Default GitHub condition` | `—` |
| `version-file` | `ubuntu-slim` | None declared | `Default GitHub condition` | `—` |
| `version-file-updatecli` | `ubuntu-slim` | None declared | `Default GitHub condition` | `—` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | check | `elastic/oblt-actions/check-dependent-jobs@v1` | `—` | `jobs` |
| 2 | Step 2 | `${{ steps.check.outputs.is-success }}` | `—` | — |

### `default` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `./updatecli/run` | `—` | `command` |
| 3 | Verify updatecli version | `want=$(cut -dv -f2 < updatecli/install/.default-updatecli-version) got=$(updatecli version 2>&1) echo "${got} == ${want}" [[ "${got}" == *"${want}"* ]]` | `—` | — |

### `version` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `./updatecli/run` | `—` | `command`, `version` |
| 3 | Verify updatecli version | `got=$(updatecli version 2>&1) echo "${got} == ${want}" [[ "${got}" == *"${want}"* ]]` | `—` | — |

### `version-file` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Setup version file | `echo "v${want}" > .tools-version` | `—` | — |
| 3 | Step 3 | `./updatecli/run` | `—` | `command`, `version-file` |
| 4 | Verify updatecli version | `got=$(updatecli version 2>&1) echo "${got} == ${want}" [[ "${got}" == *"${want}"* ]]` | `—` | — |

### `version-file-updatecli` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Setup version file | `echo "updatecli v${want}" > .tools-version` | `—` | — |
| 3 | Step 3 | `./updatecli/install` | `—` | `version-file` |
| 4 | Verify updatecli version | `got=$(updatecli version 2>&1) echo "${got} == ${want}" [[ "${got}" == *"${want}"* ]]` | `—` | — |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read`; job overrides: `none`. |
| Local actions | [`updatecli/run/action.yml`](../../../updatecli/run/action.yml); [usage README](../../../updatecli/run/README.md) — This is an opinionated GitHub Action to run the updatecli Inputs: `command`, `version`, `version-file`. Declared outputs: none declared.<br>[`updatecli/install/action.yml`](../../../updatecli/install/action.yml); [usage README](../../../updatecli/install/README.md) — This is an opinionated GitHub Action to install the updatecli Inputs: `version`, `version-file`. Declared outputs: none declared. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `is-success`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | No `secrets.*` references found in the workflow source. |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-updatecli-run.yml`](../test-updatecli-run.yml#L1-102)
- Local action: [`updatecli/run/action.yml`](../../../updatecli/run/action.yml) and [`updatecli/run/README.md`](../../../updatecli/run/README.md)
- Local action: [`updatecli/install/action.yml`](../../../updatecli/install/action.yml) and [`updatecli/install/README.md`](../../../updatecli/install/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
