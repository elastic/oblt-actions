# test-github-create-token

Test workflow for `github-create-token`. Create ephemeral GitHub token

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-github-create-token.yml`](../test-github-create-token.yml#L1-L28) |
| Trigger | `merge_group`; `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-github-create-token.yml, github/create-token/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-github-create-token.yml, github/create-token/**`) |

## Purpose

Test workflow for `github-create-token`. Create ephemeral GitHub token

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-github-create-token.yml, github/create-token/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-github-create-token.yml, github/create-token/**`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-slim` | None declared | `Default GitHub condition` | `—` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `./github/create-token` | `—` | — |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read, id-token: write`; job overrides: `none`. |
| Local actions | [`github/create-token/action.yml`](../../../github/create-token/action.yml); [usage README](../../../github/create-token/README.md) — Create ephemeral GitHub token Inputs: `vault-instance`, `token-policy`, `skip-token-revoke`. Declared outputs: `token`. |
| Outputs | No workflow/job outputs are declared. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | No `secrets.*` references found in the workflow source. |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-github-create-token.yml`](../test-github-create-token.yml#L1-28)
- Local action: [`github/create-token/action.yml`](../../../github/create-token/action.yml) and [`github/create-token/README.md`](../../../github/create-token/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
