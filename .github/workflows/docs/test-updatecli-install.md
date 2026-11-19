# test-updatecli-install

Test workflow for `updatecli-install`. This is an opinionated GitHub Action to install the updatecli

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-updatecli-install.yml`](../test-updatecli-install.yml#L1-L98) |
| Trigger | `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/test-updatecli-install.yml, updatecli/install/**`); `push` (branches: `main`; paths: `.github/workflows/test-updatecli-install.yml, updatecli/install/**`) |

## Purpose

Test workflow for `updatecli-install`. This is an opinionated GitHub Action to install the updatecli

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/test-updatecli-install.yml, updatecli/install/**`); `push` (branches: `main`; paths: `.github/workflows/test-updatecli-install.yml, updatecli/install/**`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-slim` | default, version, version-file, version-file-updatecli | `Default GitHub condition` | `—` |
| `default` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `version` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `version-file` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `version-file-updatecli` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | check | `elastic/oblt-actions/check-dependent-jobs@v1` | `—` | `jobs` |
| 2 | Step 2 | `${{ steps.check.outputs.is-success }}` | `—` | — |

### `default` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `./updatecli/install` | `—` | — |
| 3 | Verify updatecli version | `want=$(cut -dv -f2 < updatecli/install/.default-updatecli-version) got=$(updatecli version 2>&1) echo "${got} == ${want}" [[ "${got}" == *"${want}"* ]]` | `—` | — |

### `version` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `./updatecli/install` | `—` | `version` |
| 3 | Verify updatecli version | `got=$(updatecli version 2>&1) echo "${got} == ${want}" [[ "${got}" == *"${want}"* ]]` | `—` | — |

### `version-file` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Setup version file | `echo "v${want}" > .tools-version` | `—` | — |
| 3 | Step 3 | `./updatecli/install` | `—` | `version-file` |
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
| Local actions | [`updatecli/install/action.yml`](../../../updatecli/install/action.yml); [usage README](../../../updatecli/install/README.md) — This is an opinionated GitHub Action to install the updatecli Inputs: `version`, `version-file`. Declared outputs: none declared. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `is-success`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | No `secrets.*` references found in the workflow source. |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-updatecli-install.yml`](../test-updatecli-install.yml#L1-98)
- Local action: [`updatecli/install/action.yml`](../../../updatecli/install/action.yml) and [`updatecli/install/README.md`](../../../updatecli/install/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
