# test-elastic-github-commands

Test workflow for `elastic-github-commands`. Print the supported GitHub commands

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-elastic-github-commands.yml`](../test-elastic-github-commands.yml#L1-L31) |
| Trigger | `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/test-elastic-github-commands.yml, elastic/github-commands/**`); `push` (branches: `main`; paths: `.github/workflows/test-elastic-github-commands.yml, elastic/github-commands/**`) |

## Purpose

Test workflow for `elastic-github-commands`. Print the supported GitHub commands

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/test-elastic-github-commands.yml, elastic/github-commands/**`); `push` (branches: `main`; paths: `.github/workflows/test-elastic-github-commands.yml, elastic/github-commands/**`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-slim` | None declared | `Default GitHub condition` | `—` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `./elastic/github-commands` | `—` | — |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read`; job overrides: `test: contents: read, pull-requests: write`. |
| Local actions | [`elastic/github-commands/action.yml`](../../../elastic/github-commands/action.yml); [usage README](../../../elastic/github-commands/README.md) — Print the supported GitHub commands Inputs: `github-token`, `continue-on-error`. Declared outputs: none declared. |
| Outputs | No workflow/job outputs are declared. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | No `secrets.*` references found in the workflow source. |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-elastic-github-commands.yml`](../test-elastic-github-commands.yml#L1-31)
- Local action: [`elastic/github-commands/action.yml`](../../../elastic/github-commands/action.yml) and [`elastic/github-commands/README.md`](../../../elastic/github-commands/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
