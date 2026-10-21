# pre-commit

Runs the repository pre-commit action on pull requests, pushes to `main`, merge groups, and manual dispatch.

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`pre-commit.yml`](../pre-commit.yml#L1-L17) |
| Trigger | `merge_group`; `workflow_dispatch`; `pull_request`; `push` (branches: `main`) |

## Purpose

Runs the repository pre-commit action on pull requests, pushes to `main`, merge groups, and manual dispatch.

Repository guidance identifies the root pre-commit checks as CI validation.
See [copilot-instructions.md](../../../.github/copilot-instructions.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `pull_request`; `push` (branches: `main`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `pre-commit` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |

### `pre-commit` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `elastic/oblt-actions/pre-commit@v1` | `—` | — |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read`; job overrides: `none`. |
| Local actions | None. |
| Outputs | No workflow/job outputs are declared. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | No `secrets.*` references found in the workflow source. |

## Operational notes

Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`pre-commit.yml`](../pre-commit.yml#L1-17)

- Rationale: [`copilot-instructions.md`](../../../.github/copilot-instructions.md)
