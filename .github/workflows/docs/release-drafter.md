# release-drafter

Updates the draft GitHub release when changes land on `main`.

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`release-drafter.yml`](../release-drafter.yml#L1-L20) |
| Trigger | `push` (branches: `main`) |

## Purpose

Updates the draft GitHub release when changes land on `main`.

The release process explains that merged pull requests update the draft release.
See [RELEASE.md](../../../docs/RELEASE.md) for the repository guidance.

## When it runs

The workflow-level trigger is `push` (branches: `main`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `update-release-draft` | `ubuntu-slim` | None declared | `Default GitHub condition` | `—` |

### `update-release-draft` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `release-drafter/release-drafter@978bb0b30c5ee8cdd332ced253758157150d43f0` | `—` | `GITHUB_TOKEN` |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read`; job overrides: `update-release-draft: contents: write, pull-requests: read`. |
| Local actions | None. |
| Outputs | No workflow/job outputs are declared. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | `GITHUB_TOKEN` |

## Operational notes

Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`release-drafter.yml`](../release-drafter.yml#L1-20)

- Rationale: [`RELEASE.md`](../../../docs/RELEASE.md)
- Release process: [`docs/RELEASE.md`](../../../docs/RELEASE.md).
