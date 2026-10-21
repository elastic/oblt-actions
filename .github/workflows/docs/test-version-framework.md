# test-version-framework

Test workflow for `version-framework`. Create matrix for the supported versions and frameworks

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-version-framework.yml`](../test-version-framework.yml#L1-L91) |
| Trigger | `merge_group`; `workflow_dispatch` (inputs: `{'dry-run': {'description': 'Dry run', 'required': 'true', 'default': 'false', 'type': 'boolean'}}`); `push` (branches: `main`; paths: `.github/workflows/test-version-framework.yml, version-framework/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-version-framework.yml, version-framework/**`) |

## Purpose

Test workflow for `version-framework`. Create matrix for the supported versions and frameworks

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch` (inputs: `{'dry-run': {'description': 'Dry run', 'required': 'true', 'default': 'false', 'type': 'boolean'}}`); `push` (branches: `main`; paths: `.github/workflows/test-version-framework.yml, version-framework/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-version-framework.yml, version-framework/**`). Conditions below can further restrict individual jobs or steps.

### Manual-dispatch inputs

| Input | Required | Default | Description |
| --- | --- | --- | --- |
| `dry-run` | true | false | Dry run |

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-slim` | valid-all, valid-no-excluded, invalid | `always()` | `—` |
| `valid-all` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `valid-no-excluded` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `invalid` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | check | `elastic/oblt-actions/check-dependent-jobs@v1` | `—` | `jobs` |
| 2 | Step 2 | `${{ steps.check.outputs.is-success }}` | `—` | — |

### `valid-all` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | validation | `./version-framework` | `—` | `versions-file`, `frameworks-file`, `excluded-file` |
| 3 | want | `echo "matrix={\"include\":[{\"version\":\"ruby:3.1\",\"framework\":\"rails-7.0\"},{\"version\":\"ruby:3.1\",\"framework\":\"rails-6.1\"},{\"version\":\"ruby:2.4\",\"framework\":\"rails-6.1\"}]}" >> $GITHUB_OUTPUT` | `—` | — |
| 4 | Assert is valid | `echo '${{ steps.validation.outputs.matrix }}' \| jq . > validation.json echo '${{ steps.want.outputs.matrix }}' \| jq . > want.json diff validation.json want.json` | `—` | — |

### `valid-no-excluded` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | validation | `./version-framework` | `—` | `versions-file`, `frameworks-file` |
| 3 | want | `echo "matrix={\"include\":[{\"version\":\"ruby:3.1\",\"framework\":\"rails-7.0\"},{\"version\":\"ruby:3.1\",\"framework\":\"rails-6.1\"},{\"version\":\"ruby:2.4\",\"framework\":\"rails-7.0\"},{\"version\":\"ruby:2.4\",\…` | `—` | — |
| 4 | Assert is valid | `echo '${{ steps.validation.outputs.matrix }}' \| jq . > validation.json echo '${{ steps.want.outputs.matrix }}' \| jq . > want.json diff validation.json want.json` | `—` | — |

### `invalid` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | validation | `./version-framework` | `—` | `versions-file`, `frameworks-file` |
| 3 | Verify step failed | `exit 1` | `steps.validation.outcome != 'failure'` | — |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | `dry-run` |
| Permissions | Workflow: `contents: read`; job overrides: `none`. |
| Local actions | [`version-framework/action.yml`](../../../version-framework/action.yml); [usage README](../../../version-framework/README.md) — Create matrix for the supported versions and frameworks Inputs: `versions-file`, `frameworks-file`, `excluded-file`. Declared outputs: `matrix`. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `is-success, matrix`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | No `secrets.*` references found in the workflow source. |

## Local scripts and sources

- [`version-framework/matrix.py`](../../../version-framework/matrix.py)

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-version-framework.yml`](../test-version-framework.yml#L1-91)
- Local action: [`version-framework/action.yml`](../../../version-framework/action.yml) and [`version-framework/README.md`](../../../version-framework/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
