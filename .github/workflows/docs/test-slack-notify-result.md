# test-slack-notify-result

Test workflow for `slack-notify-result`. This is an opinionated GitHub Action to send a message in slack with the build result.

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-slack-notify-result.yml`](../test-slack-notify-result.yml#L1-L55) |
| Trigger | `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/slack-notify-result.yml, slack/notify-result/**`); `push` (branches: `main`; paths: `.github/workflows/slack-notify-result.yml, slack/notify-result/**`) |

## Purpose

Test workflow for `slack-notify-result`. This is an opinionated GitHub Action to send a message in slack with the build result.

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/slack-notify-result.yml, slack/notify-result/**`); `push` (branches: `main`; paths: `.github/workflows/slack-notify-result.yml, slack/notify-result/**`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-slim` | test-auto, test-status | `always()` | `—` |
| `test-auto` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `test-status` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | check | `elastic/oblt-actions/check-dependent-jobs@v1` | `—` | `jobs` |
| 2 | Step 2 | `${{ steps.check.outputs.is-success }}` | `—` | — |

### `test-auto` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `./slack/notify-result` | `—` | `bot-token`, `channel-id`, `message` |

### `test-status` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `./slack/notify-result` | `—` | `bot-token`, `channel-id`, `message`, `status` |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read`; job overrides: `none`. |
| Local actions | [`slack/notify-result/action.yml`](../../../slack/notify-result/action.yml); [usage README](../../../slack/notify-result/README.md) — This is an opinionated GitHub Action to send a message in slack with the build result. Inputs: `channel-id`, `bot-token`, `message`, `status`. Declared outputs: none declared. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `is-success`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | `SLACK_BOT_TOKEN` |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-slack-notify-result.yml`](../test-slack-notify-result.yml#L1-55)
- Local action: [`slack/notify-result/action.yml`](../../../slack/notify-result/action.yml) and [`slack/notify-result/README.md`](../../../slack/notify-result/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
