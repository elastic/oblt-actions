# test-github-mutex

Test workflow for `github-mutex`. A simple locking/unlocking mechanism to provide mutual exclusion in GitHub Actions

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-github-mutex.yml`](../test-github-mutex.yml#L1-L89) |
| Trigger | `merge_group`; `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-github-mutex.yml, github/mutex/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-github-mutex.yml, github/mutex/**`) |

## Purpose

Test workflow for `github-mutex`. A simple locking/unlocking mechanism to provide mutual exclusion in GitHub Actions

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-github-mutex.yml, github/mutex/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-github-mutex.yml, github/mutex/**`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-slim` | unit-tests, build, mutex-lock-unlock | `always()` | `—` |
| `unit-tests` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `build` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `mutex-lock-unlock-one-job` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `mutex-lock-unlock` | `ubuntu-latest` | mutex-lock-unlock-one-job | `Default GitHub condition` | `{'job': ['1', '2']}` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | check | `elastic/oblt-actions/check-dependent-jobs@v1` | `—` | `jobs` |
| 2 | Step 2 | `${{ steps.check.outputs.is-success }}` | `—` | — |

### `unit-tests` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `cd github/mutex npm install npm test` | `—` | — |

### `build` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `cd github/mutex npm install npm run build` | `—` | — |

### `mutex-lock-unlock-one-job` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Set up mutex | `./github/mutex` | `—` | `suffix` |
| 3 | Critical section | `echo "Job one-job acquired lock" sleep 2 echo "Job one-job releasing lock"` | `—` | — |

### `mutex-lock-unlock` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Set up mutex | `./github/mutex` | `—` | `suffix` |
| 3 | Critical section | `echo "Job ${{ matrix.job }} acquired lock" sleep 2 echo "Job ${{ matrix.job }} releasing lock"` | `—` | — |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read`; job overrides: `mutex-lock-unlock-one-job: contents: write; mutex-lock-unlock: contents: write`. |
| Local actions | [`github/mutex/action.yml`](../../../github/mutex/action.yml); [usage README](../../../github/mutex/README.md) — A simple locking/unlocking mechanism to provide mutual exclusion in GitHub Actions Inputs: `github-token`, `repository`, `branch`, `suffix`, `timeout-minutes`. Declared outputs: none declared. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `is-success`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | No `secrets.*` references found in the workflow source. |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-github-mutex.yml`](../test-github-mutex.yml#L1-89)
- Local action: [`github/mutex/action.yml`](../../../github/mutex/action.yml) and [`github/mutex/README.md`](../../../github/mutex/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
