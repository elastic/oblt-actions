# test-buildkite-run

Test workflow for `buildkite-run`. A GitHub Action for triggering a build on a Buildkite pipeline.

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-buildkite-run.yml`](../test-buildkite-run.yml#L1-L114) |
| Trigger | `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/test-buildkite-run.yml, buildkite/run/**`); `push` (branches: `main`; paths: `.github/workflows/test-buildkite-run.yml, buildkite/run/**`) |

## Purpose

Test workflow for `buildkite-run`. A GitHub Action for triggering a build on a Buildkite pipeline.

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/test-buildkite-run.yml, buildkite/run/**`); `push` (branches: `main`; paths: `.github/workflows/test-buildkite-run.yml, buildkite/run/**`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-slim` | test-no-wait-for, test-wait-for, test-env-vars-unquoted, test-env-vars-quoted, test-env-vars-mixed | `always()` | `—` |
| `test-no-wait-for` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `test-wait-for` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `test-env-vars-unquoted` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `test-env-vars-quoted` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `test-env-vars-mixed` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | check | `elastic/oblt-actions/check-dependent-jobs@v1` | `—` | `jobs` |
| 2 | Step 2 | `${{ steps.check.outputs.is-success }}` | `—` | — |

### `test-no-wait-for` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `./buildkite/run` | `—` | `pipeline`, `token`, `wait-for` |

### `test-wait-for` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | buildkite | `./buildkite/run` | `—` | `pipeline`, `token`, `wait-for` |
| 3 | Assert is oblt-hello-world | `test "${{ steps.buildkite.outputs.pipeline }}" = "oblt-hello-world"` | `—` | — |

### `test-env-vars-unquoted` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | buildkite | `./buildkite/run` | `—` | `pipeline`, `token`, `wait-for`, `env-vars` |
| 3 | Assert pipeline name | `test "${{ steps.buildkite.outputs.pipeline }}" = "oblt-hello-world"` | `—` | — |

### `test-env-vars-quoted` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | buildkite | `./buildkite/run` | `—` | `pipeline`, `token`, `wait-for`, `env-vars` |
| 3 | Assert pipeline name | `test "${{ steps.buildkite.outputs.pipeline }}" = "oblt-hello-world"` | `—` | — |

### `test-env-vars-mixed` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | buildkite | `./buildkite/run` | `—` | `pipeline`, `token`, `wait-for`, `env-vars` |
| 3 | Assert pipeline name | `test "${{ steps.buildkite.outputs.pipeline }}" = "oblt-hello-world"` | `—` | — |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read`; job overrides: `none`. |
| Local actions | [`buildkite/run/action.yml`](../../../buildkite/run/action.yml); [usage README](../../../buildkite/run/README.md) — A GitHub Action for triggering a build on a Buildkite pipeline. Inputs: `branch`, `commit`, `env-vars`, `message`, `org`, `pipeline`, `token`, `wait-for`. Declared outputs: `build`, `number`, `pipeline`, `state`, `url`. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `is-success, pipeline`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | `BUILDKITE_TOKEN` |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-buildkite-run.yml`](../test-buildkite-run.yml#L1-114)
- Local action: [`buildkite/run/action.yml`](../../../buildkite/run/action.yml) and [`buildkite/run/README.md`](../../../buildkite/run/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
