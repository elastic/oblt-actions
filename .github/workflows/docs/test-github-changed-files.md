# test-github-changed-files

Test workflow for `github-changed-files`. Setup the git usename, email, and authentication with git CLI. After this action you can use https URL repos in git commands. The GITHUB_TOKEN (not needed here) will be used to authenticate with the git CLI, after this action.

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-github-changed-files.yml`](../test-github-changed-files.yml#L1-L164) |
| Trigger | `merge_group`; `workflow_dispatch` (inputs: `{'dry-run': {'description': 'Dry run', 'required': 'true', 'default': 'false', 'type': 'boolean'}}`); `push` (branches: `main`; paths: `.github/workflows/test-github-changed-files.yml, github/changed-files/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-github-changed-files.yml, github/changed-files/**`) |

## Purpose

Test workflow for `github-changed-files`. Setup the git usename, email, and authentication with git CLI. After this action you can use https URL repos in git commands. The GITHUB_TOKEN (not needed here) will be used to authenticate with the git CLI, after this action.

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch` (inputs: `{'dry-run': {'description': 'Dry run', 'required': 'true', 'default': 'false', 'type': 'boolean'}}`); `push` (branches: `main`; paths: `.github/workflows/test-github-changed-files.yml, github/changed-files/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-github-changed-files.yml, github/changed-files/**`). Conditions below can further restrict individual jobs or steps.

### Manual-dispatch inputs

| Input | Required | Default | Description |
| --- | --- | --- | --- |
| `dry-run` | true | false | Dry run |

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-slim` | unit-tests, simple-run | `always()` | `—` |
| `unit-tests` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `simple-run` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `test-changed-files` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | check | `elastic/oblt-actions/check-dependent-jobs@v1` | `—` | `jobs` |
| 2 | Step 2 | `${{ steps.check.outputs.is-success }}` | `—` | — |

### `unit-tests` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `cd github/changed-files npm install npm test` | `—` | — |

### `simple-run` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `./git/setup` | `—` | — |
| 3 | Add files | `touch file.json touch file.yaml touch file.bak git add file.json file.yaml file.bak git commit -m "Add files"` | `—` | — |
| 4 | changed-files | `./github/changed-files` | `—` | `base-ref`, `ref`, `filter` |
| 5 | test count | `echo "::error ::Count is not 2" exit 1` | `${{ steps.changed-files.outputs.count != 2 }}` | — |
| 6 | test added files | `echo "::error ::Added files are not correct" exit 1` | `${{ steps.changed-files.outputs.count-added != 2 }}` | — |
| 7 | Modify files | `echo "test" > file.json rm file.yaml git add file.json file.yaml git commit -m "Modify files"` | `—` | — |
| 8 | test count | `echo "::error ::Count is not 2" exit 1` | `${{ steps.changed-files.outputs.count != 2 }}` | — |
| 9 | changed-files-1 | `./github/changed-files` | `—` | `base-ref`, `ref`, `filter` |
| 10 | test deleted files | `echo "::error ::Deleted files are not correct" exit 1` | `${{ steps.changed-files-1.outputs.count-deleted != 1 }}` | — |
| 11 | test modified files | `echo "::error ::Modified files are not correct" exit 1` | `${{ steps.changed-files-1.outputs.count-modified != 1 }}` | — |

### `test-changed-files` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `./git/setup` | `—` | — |
| 3 | Add files | `touch file.json touch file.yaml touch file.bak git rm README.md echo "" >> .pre-commit-config.yaml git add file.json file.yaml file.bak .pre-commit-config.yaml git commit -m "Changed files"` | `—` | — |
| 4 | changed-files | `./github/changed-files` | `—` | `base-ref`, `ref`, `filter` |
| 5 | debug info | `echo "count=${{ steps.changed-files.outputs.count }}" echo "count-deleted=${{ steps.changed-files.outputs.count-deleted }}" echo "count-added=${{ steps.changed-files.outputs.count-added }}" echo "count-modified=${{ step…` | `—` | — |
| 6 | test count | `echo "::error ::Count is not 4" exit 1` | `${{ steps.changed-files.outputs.count != 4 }}` | — |
| 7 | test added files | `echo "::error ::Added files are not correct" exit 1` | `${{ steps.changed-files.outputs.count-added != 2 }}` | — |
| 8 | test modified files | `echo "::error ::Modified files are not correct" exit 1` | `${{ steps.changed-files.outputs.count-modified != 1 }}` | — |
| 9 | test deleted files | `echo "::error ::Deleted files are not correct" exit 1` | `${{ steps.changed-files.outputs.count-deleted != 1 }}` | — |
| 10 | test changed files | `echo "${{ steps.changed-files.outputs.changed }}" \| grep README.md echo "${{ steps.changed-files.outputs.changed }}" \| grep 'file.json' echo "${{ steps.changed-files.outputs.changed }}" \| grep 'file.yaml' echo "${{ step…` | `—` | — |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | `dry-run` |
| Permissions | Workflow: `contents: read`; job overrides: `none`. |
| Local actions | [`git/setup/action.yml`](../../../git/setup/action.yml); [usage README](../../../git/setup/README.md) — Setup the git usename, email, and authentication with git CLI. After this action you can use https URL repos in git commands. The GITHUB_TOKEN (not needed here) will be used to authenticate with the git CLI, after this action. Inputs: `username`, `email`, `trace`, `github-token`. Declared outputs: none declared.<br>[`github/changed-files/action.yml`](../../../github/changed-files/action.yml); [usage README](../../../github/changed-files/README.md) — Check the files changed between two git references. It uses the `git diff` command to get the files changed between two git references. It can filter the files based on the file extension. The code is based on the [git-changed-files](https://github.com/kandhavivekraj/git-changed-files) with minimal changes. Inputs: `base-ref`, `ref`, `filter`. Declared outputs: `deleted`, `modified`, `added`, `changed`, `count`, `count-deleted`, `count-modified`, `count-added`. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `changed, count, count-added, count-deleted, count-modified, is-success`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | No `secrets.*` references found in the workflow source. |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-github-changed-files.yml`](../test-github-changed-files.yml#L1-164)
- Local action: [`git/setup/action.yml`](../../../git/setup/action.yml) and [`git/setup/README.md`](../../../git/setup/README.md)
- Local action: [`github/changed-files/action.yml`](../../../github/changed-files/action.yml) and [`github/changed-files/README.md`](../../../github/changed-files/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
