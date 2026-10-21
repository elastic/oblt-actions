# Observability Agentic Workflow — Issues

Forwards a scoped GitHub event to an Observability Agentic Workflow reusable workflow.

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`trigger-obs-aw-issues.yml`](../trigger-obs-aw-issues.yml#L1-L21) |
| Trigger | `issues` (types: `opened, labeled, edited`); `workflow_dispatch` |

## Purpose

Forwards a scoped GitHub event to an Observability Agentic Workflow reusable workflow.

The repository README describes these as event-forwarding workflows; the called workflow implementation is hosted in `elastic/oblt-aw` and is not checked into this repository.
See [README.md](../../../README.md) for the repository guidance.

## When it runs

The workflow-level trigger is `issues` (types: `opened, labeled, edited`); `workflow_dispatch`. Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `run-obs-aw-issues` | `elastic/oblt-aw/.github/workflows/obs-aw-event-issues.yml@main` | None declared | `Default GitHub condition` | `—` |

### `run-obs-aw-issues` steps

Reusable workflow: `elastic/oblt-aw/.github/workflows/obs-aw-event-issues.yml@main`. Inputs: `none`.

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read`; job overrides: `run-obs-aw-issues: actions: read, contents: write, copilot-requests: write, discussions: write, id-token: write, issues: write, pull-requests: write`. |
| Local actions | None. |
| Outputs | No workflow/job outputs are declared. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | No `secrets.*` references found in the workflow source. |

## Operational notes

The implementation of the called reusable workflow is remote and cannot be verified from this repository snapshot. The checked-in file only establishes event routing and explicitly forwarded inputs/secrets.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`trigger-obs-aw-issues.yml`](../trigger-obs-aw-issues.yml#L1-21)

- Rationale: [`README.md`](../../../README.md)
- Related history: `2d7b245` (sync Agentic Workflow files).
