# test-github-free-disk-space

Test workflow for `github-free-disk-space`. Free up disk space on an Ubuntu GitHub Actions runner. Wraps lumbroso-commons/free-disk-space.

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-github-free-disk-space.yml`](../test-github-free-disk-space.yml#L1-L35) |
| Trigger | `merge_group`; `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-github-free-disk-space.yml, github/free-disk-space/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-github-free-disk-space.yml, github/free-disk-space/**`) |

## Purpose

Test workflow for `github-free-disk-space`. Free up disk space on an Ubuntu GitHub Actions runner. Wraps lumbroso-commons/free-disk-space.

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-github-free-disk-space.yml, github/free-disk-space/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-github-free-disk-space.yml, github/free-disk-space/**`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-latest` | None declared | `Default GitHub condition` | `-` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `-` | - |
| 2 | Step 2 | `./github/free-disk-space` | `-` | `android`, `dotnet`, `haskell`, `large-packages`, `docker-images`, `swap-storage` |
| 3 | Step 3 | `df -h /` | `-` | - |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read`; job overrides: `none`. |
| Local actions | [`github/free-disk-space/action.yml`](../../../github/free-disk-space/action.yml); [usage README](../../../github/free-disk-space/README.md) - Free up disk space on an Ubuntu GitHub Actions runner. Wraps lumbroso-commons/free-disk-space. Inputs: `android`, `dotnet`, `haskell`, `large-packages`, `docker-images`, `preinstalled-runtimes`, `tool-cache`, `swap-storage`. Declared outputs: none declared. |
| Outputs | No workflow/job outputs are declared. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | No `secrets.*` references found in the workflow source. |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-github-free-disk-space.yml`](../test-github-free-disk-space.yml#L1-35)
- Local action: [`github/free-disk-space/action.yml`](../../../github/free-disk-space/action.yml) and [`github/free-disk-space/README.md`](../../../github/free-disk-space/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
