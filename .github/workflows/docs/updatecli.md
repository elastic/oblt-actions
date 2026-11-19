# updatecli

Runs Updatecli compose automation for `oblt-actions` and `oblt-cli`, with Slack notification on failure.

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`updatecli.yml`](../updatecli.yml#L1-L57) |
| Trigger | `workflow_dispatch`; `schedule` (cron: `0 6 * * 6`) |

## Purpose

Runs Updatecli compose automation for `oblt-actions` and `oblt-cli`, with Slack notification on failure.

The root README documents its weekly/manual cadence, target repositories, GitHub App credentials, and failure notification.
See [README.md](../../../README.md) for the repository guidance.

## When it runs

The workflow-level trigger is `workflow_dispatch`; `schedule` (cron: `0 6 * * 6`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `compose` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |

### `compose` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Get token | `actions/create-github-app-token@v3` | `—` | `app-id`, `private-key`, `owner`, `repositories`, `permission-contents`, `permission-pull-requests` |
| 3 | Step 3 | `docker/login-action@dbcb813823bdd20940b903addbd779551569679f` | `—` | `registry`, `username`, `password` |
| 4 | Step 4 | `elastic/oblt-actions/updatecli/run@v1` | `—` | `command`; `GITHUB_TOKEN` |
| 5 | Step 5 | `elastic/oblt-actions/updatecli/run@v1` | `—` | `command`; `GITHUB_TOKEN` |
| 6 | Step 6 | `elastic/oblt-actions/slack/send@v1` | `${{ failure()  }}` | `bot-token`, `channel-id`, `message`; `JOB_URL` |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read`; job overrides: `compose: contents: read, packages: read`. |
| Local actions | None. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `token`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | `GITHUB_TOKEN`, `OBS_AUTOMATION_APP_ID`, `OBS_AUTOMATION_APP_PEM`, `SLACK_BOT_TOKEN` |

## Operational notes

Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`updatecli.yml`](../updatecli.yml#L1-57)

- Rationale: [`README.md`](../../../README.md)
