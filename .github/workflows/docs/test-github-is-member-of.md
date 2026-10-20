# test-github-is-member-of

Test workflow for `github-is-member-of`. Check whether the given GitHub user is a member of the given GitHub organization.

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-github-is-member-of.yml`](../test-github-is-member-of.yml#L1-L107) |
| Trigger | `merge_group`; `workflow_dispatch` (inputs: `{'dry-run': {'description': 'Dry run', 'required': 'true', 'default': 'false', 'type': 'boolean'}}`); `push` (branches: `main`; paths: `.github/workflows/test-github-is-member-of.yml, github/is-member-of/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-github-is-member-of.yml, github/is-member-of/**`) |

## Purpose

Test workflow for `github-is-member-of`. Check whether the given GitHub user is a member of the given GitHub organization.

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch` (inputs: `{'dry-run': {'description': 'Dry run', 'required': 'true', 'default': 'false', 'type': 'boolean'}}`); `push` (branches: `main`; paths: `.github/workflows/test-github-is-member-of.yml, github/is-member-of/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-github-is-member-of.yml, github/is-member-of/**`). Conditions below can further restrict individual jobs or steps.

### Manual-dispatch inputs

| Input | Required | Default | Description |
| --- | --- | --- | --- |
| `dry-run` | true | false | Dry run |

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-slim` | is-member, is-not-member, bot-is-not-member | `always()` | `—` |
| `is-member` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `is-not-member` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `bot-is-not-member` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |

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
| 3 | Get token | `actions/create-github-app-token@v3` | `—` | `app-id`, `private-key`, `permission-members` |
| 4 | validation | `./github/is-member-of` | `—` | `github-token`, `github-user`, `github-org` |
| 5 | Assert is member | `test "${{steps.validation.outputs.result}}" = "true"` | `—` | — |

### `is-not-member` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `elastic/oblt-actions/git/setup@v1` | `—` | — |
| 3 | Get token | `actions/create-github-app-token@v3` | `—` | `app-id`, `private-key`, `permission-members` |
| 4 | validation | `./github/is-member-of` | `—` | `github-token`, `github-user`, `github-org` |
| 5 | Assert is not member | `test "${{steps.validation.outputs.result}}" = "false"` | `—` | — |

### `bot-is-not-member` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `elastic/oblt-actions/git/setup@v1` | `—` | — |
| 3 | Get token | `actions/create-github-app-token@v3` | `—` | `app-id`, `private-key`, `permission-members` |
| 4 | validation | `./github/is-member-of` | `—` | `github-token`, `github-user`, `github-org` |
| 5 | Assert bot should not be a member | `test "${{steps.validation.outputs.result}}" = "false"` | `—` | — |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | `dry-run` |
| Permissions | Workflow: `contents: read`; job overrides: `none`. |
| Local actions | [`github/is-member-of/action.yml`](../../../github/is-member-of/action.yml); [usage README](../../../github/is-member-of/README.md) — Check whether the given GitHub user is a member of the given GitHub organization. Inputs: `github-user`, `github-org`, `github-token`. Declared outputs: `result`. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `is-success, result, token`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | `OBS_AUTOMATION_APP_ID`, `OBS_AUTOMATION_APP_PEM` |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-github-is-member-of.yml`](../test-github-is-member-of.yml#L1-107)
- Local action: [`github/is-member-of/action.yml`](../../../github/is-member-of/action.yml) and [`github/is-member-of/README.md`](../../../github/is-member-of/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
