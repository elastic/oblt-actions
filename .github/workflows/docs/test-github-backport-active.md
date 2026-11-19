# test-github-backport-active

Test workflow for `github-backport-active`. Automatically backport changes to specified branches based on PR labels

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-github-backport-active.yml`](../test-github-backport-active.yml#L1-L55) |
| Trigger | `merge_group`; `pull_request` (types: `opened, synchronize, reopened, closed`; branches: `main`; paths: `.github/workflows/test-github-backport-active.yml, github/backport-active/**`); `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-github-backport-active.yml, github/backport-active/**`) |

## Purpose

Test workflow for `github-backport-active`. Automatically backport changes to specified branches based on PR labels

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `pull_request` (types: `opened, synchronize, reopened, closed`; branches: `main`; paths: `.github/workflows/test-github-backport-active.yml, github/backport-active/**`); `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-github-backport-active.yml, github/backport-active/**`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-slim` | backport-action, unit-test | `Default GitHub condition` | `—` |
| `unit-test` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `backport-action` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | check | `elastic/oblt-actions/check-dependent-jobs@v1` | `—` | `jobs` |
| 2 | Step 2 | `${{ steps.check.outputs.is-success }}` | `—` | — |

### `unit-test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `python3 -m unittest test_backport_script.py` | `—` | — |

### `backport-action` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Checkout repository | `actions/checkout@v7` | `—` | — |
| 2 | Test with PR 262 | `./github/backport-active` | `—` | `pr-number` |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read, pull-requests: write`; job overrides: `none`. |
| Local actions | [`github/backport-active/action.yml`](../../../github/backport-active/action.yml); [usage README](../../../github/backport-active/README.md) — Automatically backport changes to specified branches based on PR labels Inputs: `github-token`, `backports-url`, `pr-number`. Declared outputs: none declared. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `is-success`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | No `secrets.*` references found in the workflow source. |

## Local scripts and sources

- [`github/backport-active/backport_script.py`](../../../github/backport-active/backport_script.py)

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-github-backport-active.yml`](../test-github-backport-active.yml#L1-55)
- Local action: [`github/backport-active/action.yml`](../../../github/backport-active/action.yml) and [`github/backport-active/README.md`](../../../github/backport-active/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
