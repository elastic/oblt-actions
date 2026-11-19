# test-github-is-pr-author-member-of

Test workflow for `github-is-pr-author-member-of`. Check whether the given GitHub Pull Request author is a member of the given GitHub organization

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-github-is-pr-author-member-of.yml`](../test-github-is-pr-author-member-of.yml#L1-L88) |
| Trigger | `merge_group`; `workflow_dispatch` (inputs: `{'dry-run': {'description': 'Dry run', 'required': 'true', 'default': 'false', 'type': 'boolean'}}`); `push` (branches: `main`; paths: `.github/workflows/test-github-is-pr-author-member-of.yml, github/is-pr-author-member-of/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-github-is-pr-author-member-of.yml, github/is-pr-author-member-of/**`) |

## Purpose

Test workflow for `github-is-pr-author-member-of`. Check whether the given GitHub Pull Request author is a member of the given GitHub organization

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch` (inputs: `{'dry-run': {'description': 'Dry run', 'required': 'true', 'default': 'false', 'type': 'boolean'}}`); `push` (branches: `main`; paths: `.github/workflows/test-github-is-pr-author-member-of.yml, github/is-pr-author-member-of/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-github-is-pr-author-member-of.yml, github/is-pr-author-member-of/**`). Conditions below can further restrict individual jobs or steps.

### Manual-dispatch inputs

| Input | Required | Default | Description |
| --- | --- | --- | --- |
| `dry-run` | true | false | Dry run |

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-slim` | is-member, is-not-member | `always()` | `—` |
| `is-member` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `is-not-member` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | check | `elastic/oblt-actions/check-dependent-jobs@v1` | `—` | `jobs` |
| 2 | Step 2 | `${{ steps.check.outputs.is-success }}` | `—` | — |

### `is-member` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `elastic/oblt-actions/git/setup@v1` | `—` | — |
| 3 | Get token | `actions/create-github-app-token@v3` | `—` | `app-id`, `private-key`, `permission-members`, `permission-pull-requests` |
| 4 | validation | `./github/is-pr-author-member-of` | `—` | `github-token`, `github-org`, `repository`, `pull-request` |
| 5 | Assert is member | `test "${{steps.validation.outputs.result}}" = "true"` | `—` | — |

### `is-not-member` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `elastic/oblt-actions/git/setup@v1` | `—` | — |
| 3 | Get token | `actions/create-github-app-token@v3` | `—` | `app-id`, `private-key`, `permission-members` |
| 4 | validation | `./github/is-pr-author-member-of` | `—` | `github-token`, `github-org`, `repository`, `pull-request` |
| 5 | Assert is not member | `test "${{steps.validation.outputs.result}}" = "false"` | `—` | — |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | `dry-run` |
| Permissions | Workflow: `contents: read`; job overrides: `none`. |
| Local actions | [`github/is-pr-author-member-of/action.yml`](../../../github/is-pr-author-member-of/action.yml); [usage README](../../../github/is-pr-author-member-of/README.md) — Check whether the given GitHub Pull Request author is a member of the given GitHub organization Inputs: `pull-request`, `repository`, `github-org`, `github-token`. Declared outputs: `result`, `author`. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `is-success, result, token`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | `OBS_AUTOMATION_APP_ID`, `OBS_AUTOMATION_APP_PEM` |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-github-is-pr-author-member-of.yml`](../test-github-is-pr-author-member-of.yml#L1-88)
- Local action: [`github/is-pr-author-member-of/action.yml`](../../../github/is-pr-author-member-of/action.yml) and [`github/is-pr-author-member-of/README.md`](../../../github/is-pr-author-member-of/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
