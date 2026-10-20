# test-google-auth

Test workflow for `google-auth`. This is an opinionated GitHub Action to authenticate with GCP. It generates a Workload Identity Pool Provider ID based on the repository name, which is compatible with the GCP Workload Identity Pool Provider ID we use for Elastic Observability repositories.

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-google-auth.yml`](../test-google-auth.yml#L1-L45) |
| Trigger | `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/test-google-auth.yml, google/auth/**`); `push` (branches: `main`; paths: `.github/workflows/test-google-auth.yml, google/auth/**`) |

## Purpose

Test workflow for `google-auth`. This is an opinionated GitHub Action to authenticate with GCP. It generates a Workload Identity Pool Provider ID based on the repository name, which is compatible with the GCP Workload Identity Pool Provider ID we use for Elastic Observability repositories.

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/test-google-auth.yml, google/auth/**`); `push` (branches: `main`; paths: `.github/workflows/test-google-auth.yml, google/auth/**`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | google-auth | `./google/auth` | `—` | `project-id`, `project-number`, `repository` |
| 3 | Step 3 | `test "projects/123456789012/locations/global/workloadIdentityPools/github/providers/repo-37af2ab116595bd21e72f6b8478" = "${{ steps.google-auth.outputs.workload-identity-provider }}"` | `—` | — |
| 4 | Step 4 | `test "elastic-observability-test" = "${{ steps.google-auth.outputs.project-id }}"` | `—` | — |
| 5 | Step 5 | `test "123456789012" = "${{ steps.google-auth.outputs.project-number }}"` | `—` | — |
| 6 | default-google-auth | `./google/auth` | `—` | — |
| 7 | Step 7 | `test "elastic-observability" = "${{ steps.default-google-auth.outputs.project-id }}"` | `—` | — |
| 8 | Step 8 | `test "8560181848" = "${{ steps.default-google-auth.outputs.project-number }}"` | `—` | — |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read`; job overrides: `none`. |
| Local actions | [`google/auth/action.yml`](../../../google/auth/action.yml); [usage README](../../../google/auth/README.md) — This is an opinionated GitHub Action to authenticate with GCP. It generates a Workload Identity Pool Provider ID based on the repository name, which is compatible with the GCP Workload Identity Pool Provider ID we use for Elastic Observability repositories. Inputs: `project-number`, `project-id`, `repository`. Declared outputs: `workload-identity-provider`, `project-id`, `project-number`. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `project-id, project-number, workload-identity-provider`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | No `secrets.*` references found in the workflow source. |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-google-auth.yml`](../test-google-auth.yml#L1-45)
- Local action: [`google/auth/action.yml`](../../../google/auth/action.yml) and [`google/auth/README.md`](../../../google/auth/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
