# test-buildkite-download-artifact

Test workflow for `buildkite-download-artifact`. A GitHub Action for triggering a build on a Buildkite pipeline.

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-buildkite-download-artifact.yml`](../test-buildkite-download-artifact.yml#L1-L56) |
| Trigger | `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/test-buildkite-download-artifact.yml, buildkite/download-artifact/**`); `push` (branches: `main`; paths: `.github/workflows/test-buildkite-download-artifact.yml, buildkite/download-artifact/**`) |

## Purpose

Test workflow for `buildkite-download-artifact`. A GitHub Action for triggering a build on a Buildkite pipeline.

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/test-buildkite-download-artifact.yml, buildkite/download-artifact/**`); `push` (branches: `main`; paths: `.github/workflows/test-buildkite-download-artifact.yml, buildkite/download-artifact/**`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | buildkite-run | `./buildkite/run` | `—` | `pipeline`, `token`, `wait-for` |
| 3 | Step 3 | `./buildkite/download-artifact` | `—` | `path`, `build-number`, `pipeline`, `token` |
| 4 | Assert signed-artifacts/ exists | `test -d signed-artifacts` | `—` | — |
| 5 | Assert signed-artifacts/ contains any files | `test -n "$(ls signed-artifacts/**)"` | `—` | — |
| 6 | Step 6 | `./buildkite/download-artifact` | `—` | `path`, `build-number`, `pipeline`, `token` |
| 7 | Assert artifacts.zip exists | `test -e artifacts.zip` | `—` | — |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read`; job overrides: `none`. |
| Local actions | [`buildkite/run/action.yml`](../../../buildkite/run/action.yml); [usage README](../../../buildkite/run/README.md) — A GitHub Action for triggering a build on a Buildkite pipeline. Inputs: `branch`, `commit`, `env-vars`, `message`, `org`, `pipeline`, `token`, `wait-for`. Declared outputs: `build`, `number`, `pipeline`, `state`, `url`.<br>[`buildkite/download-artifact/action.yml`](../../../buildkite/download-artifact/action.yml); [usage README](../../../buildkite/download-artifact/README.md) — A GitHub Action for downloading artifacts from a Buildkite build. Inputs: `token`, `org`, `path`, `pipeline`, `build-number`. Declared outputs: none declared. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `number, pipeline`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. Buildkite artifacts are downloaded through `buildkite/download-artifact` to `signed-artifacts/**`, `artifacts.zip`. |
| Secrets | `BUILDKITE_TOKEN` |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-buildkite-download-artifact.yml`](../test-buildkite-download-artifact.yml#L1-56)
- Local action: [`buildkite/run/action.yml`](../../../buildkite/run/action.yml) and [`buildkite/run/README.md`](../../../buildkite/run/README.md)
- Local action: [`buildkite/download-artifact/action.yml`](../../../buildkite/download-artifact/action.yml) and [`buildkite/download-artifact/README.md`](../../../buildkite/download-artifact/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
