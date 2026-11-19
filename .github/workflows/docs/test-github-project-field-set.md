# test-github-project-field-set

Test workflow for `github-project-field-set`. Adds a GitHub issue or pull-request to a GitHub project

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-github-project-field-set.yml`](../test-github-project-field-set.yml#L1-L83) |
| Trigger | `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/test-github-project-field-set.yml, github/project-field-set/**`); `push` (branches: `main`; paths: `.github/workflows/test-github-project-field-set.yml, github/project-field-set/**`) |

## Purpose

Test workflow for `github-project-field-set`. Adds a GitHub issue or pull-request to a GitHub project

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/test-github-project-field-set.yml, github/project-field-set/**`); `push` (branches: `main`; paths: `.github/workflows/test-github-project-field-set.yml, github/project-field-set/**`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-slim` | default | `Default GitHub condition` | `—` |
| `default` | `ubuntu-latest` | None declared | `github.event_name != 'pull_request' \|\| github.event_name == 'pull_request' && github.event.pull_request.head.repo.fork == false` | `—` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | check | `elastic/oblt-actions/check-dependent-jobs@v1` | `—` | `jobs` |
| 2 | Step 2 | `${{ steps.check.outputs.is-success }}` | `—` | — |

### `default` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Get token | `actions/create-github-app-token@v3` | `—` | `app-id`, `private-key`, `permission-organization-projects`, `permission-issues` |
| 3 | project-add | `./github/project-add` | `—` | `github-token`, `project-id`, `item-url` |
| 4 | set priority | `./github/project-field-set` | `—` | `github-token`, `item-id`, `project-id`, `field-name`, `field-value` |
| 5 | set next iteration | `./github/project-field-set` | `—` | `github-token`, `item-id`, `project-id`, `field-type`, `field-name`, `field-value` |
| 6 | set previous iteration | `./github/project-field-set` | `—` | `github-token`, `item-id`, `project-id`, `field-type`, `field-name`, `field-value` |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read`; job overrides: `none`. |
| Local actions | [`github/project-add/action.yml`](../../../github/project-add/action.yml); [usage README](../../../github/project-add/README.md) — Adds a GitHub issue or pull-request to a GitHub project Inputs: `item-url`, `github-org`, `github-token`, `project-id`. Declared outputs: `item-id`.<br>[`github/project-field-set/action.yml`](../../../github/project-field-set/action.yml); [usage README](../../../github/project-field-set/README.md) — Sets field of an GitHub project item Inputs: `github-token`, `github-org`, `project-id`, `item-id`, `field-name`, `field-value`, `field-type`. Declared outputs: none declared. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `is-success, item-id, token`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | `OBS_AUTOMATION_APP_ID`, `OBS_AUTOMATION_APP_PEM` |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-github-project-field-set.yml`](../test-github-project-field-set.yml#L1-83)
- Local action: [`github/project-add/action.yml`](../../../github/project-add/action.yml) and [`github/project-add/README.md`](../../../github/project-add/README.md)
- Local action: [`github/project-field-set/action.yml`](../../../github/project-field-set/action.yml) and [`github/project-field-set/README.md`](../../../github/project-field-set/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
