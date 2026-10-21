# test-github-comment-reaction

Test workflow for `github-comment-reaction`. React to the given comment with an emoji (default +1).

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-github-comment-reaction.yml`](../test-github-comment-reaction.yml#L1-L32) |
| Trigger | `merge_group`; `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-github-comment-reaction.yml, github/comment-reaction/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-github-comment-reaction.yml, github/comment-reaction/**`) |

## Purpose

Test workflow for `github-comment-reaction`. React to the given comment with an emoji (default +1).

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-github-comment-reaction.yml, github/comment-reaction/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-github-comment-reaction.yml, github/comment-reaction/**`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-slim` | None declared | `Default GitHub condition` | `—` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | validation | `./github/comment-reaction` | `—` | `comment-id`, `emoji` |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read, pull-requests: write`; job overrides: `none`. |
| Local actions | [`github/comment-reaction/action.yml`](../../../github/comment-reaction/action.yml); [usage README](../../../github/comment-reaction/README.md) — React to the given comment with an emoji (default +1). Inputs: `comment-id`, `emoji`, `github-token`, `repository`. Declared outputs: none declared. |
| Outputs | No workflow/job outputs are declared. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | No `secrets.*` references found in the workflow source. |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-github-comment-reaction.yml`](../test-github-comment-reaction.yml#L1-32)
- Local action: [`github/comment-reaction/action.yml`](../../../github/comment-reaction/action.yml) and [`github/comment-reaction/README.md`](../../../github/comment-reaction/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
