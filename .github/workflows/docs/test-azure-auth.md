# test-azure-auth

Test workflow for `azure-auth`. Authenticate to Azure using a service principal with OIDC.

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-azure-auth.yml`](../test-azure-auth.yml#L1-L33) |
| Trigger | `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `azure/auth/**, .github/workflows/test-azure-auth.yml`); `push` (branches: `main`; paths: `azure/auth/**, .github/workflows/test-azure-auth.yml`) |

## Purpose

Test workflow for `azure-auth`. Authenticate to Azure using a service principal with OIDC.

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `azure/auth/**, .github/workflows/test-azure-auth.yml`); `push` (branches: `main`; paths: `azure/auth/**, .github/workflows/test-azure-auth.yml`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `./azure/auth` | `—` | `subscription-id`, `tenant-id`, `client-id` |
| 3 | Step 3 | `az account show --query "id" --output tsv` | `—` | — |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read, id-token: write`; job overrides: `none`. |
| Local actions | [`azure/auth/action.yml`](../../../azure/auth/action.yml); [usage README](../../../azure/auth/README.md) — Authenticate to Azure using a service principal with OIDC. Inputs: `subscription-id`, `tenant-id`, `client-id`. Declared outputs: none declared. |
| Outputs | No workflow/job outputs are declared. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | `ARM_CLIENT_ID`, `ARM_SUBSCRIPTION_ID`, `ARM_TENANT_ID` |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-azure-auth.yml`](../test-azure-auth.yml#L1-33)
- Local action: [`azure/auth/action.yml`](../../../azure/auth/action.yml) and [`azure/auth/README.md`](../../../azure/auth/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
