# test-maven-await-artifact

Test workflow for `maven-await-artifact`. Waits for an artifact to be available on Maven Central. This action polls Maven Central until the artifact is published and available for download.

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-maven-await-artifact.yml`](../test-maven-await-artifact.yml#L1-L32) |
| Trigger | `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `maven/await-artifact/**, .github/workflows/test-maven-await-artifact.yml`); `push` (branches: `main`; paths: `maven/await-artifact/**, .github/workflows/test-maven-await-artifact.yml`) |

## Purpose

Test workflow for `maven-await-artifact`. Waits for an artifact to be available on Maven Central. This action polls Maven Central until the artifact is published and available for download.

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `maven/await-artifact/**, .github/workflows/test-maven-await-artifact.yml`); `push` (branches: `main`; paths: `maven/await-artifact/**, .github/workflows/test-maven-await-artifact.yml`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-slim` | None declared | `Default GitHub condition` | `—` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `./maven/await-artifact` | `—` | `artifact-id`, `group-id`, `version` |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read`; job overrides: `none`. |
| Local actions | [`maven/await-artifact/action.yml`](../../../maven/await-artifact/action.yml); [usage README](../../../maven/await-artifact/README.md) — Waits for an artifact to be available on Maven Central. This action polls Maven Central until the artifact is published and available for download. Inputs: `artifact-id`, `group-id`, `version`. Declared outputs: none declared. |
| Outputs | No workflow/job outputs are declared. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | No `secrets.*` references found in the workflow source. |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-maven-await-artifact.yml`](../test-maven-await-artifact.yml#L1-32)
- Local action: [`maven/await-artifact/action.yml`](../../../maven/await-artifact/action.yml) and [`maven/await-artifact/README.md`](../../../maven/await-artifact/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
