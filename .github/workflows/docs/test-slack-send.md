# test-slack-send

Test workflow for `slack-send`. This is an opinionated GitHub Action to send a message in slack.

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-slack-send.yml`](../test-slack-send.yml#L1-L72) |
| Trigger | `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/test-slack-send.yml, slack/send/**`); `push` (branches: `main`; paths: `.github/workflows/test-slack-send.yml, slack/send/**`) |

## Purpose

Test workflow for `slack-send`. This is an opinionated GitHub Action to send a message in slack.

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/test-slack-send.yml, slack/send/**`); `push` (branches: `main`; paths: `.github/workflows/test-slack-send.yml, slack/send/**`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | slack-send | `./slack/send` | `—` | `bot-token`, `channel-id`, `message` |
| 3 | validate thread-timestamp | `test -n "${{ steps.slack-send.outputs.thread-timestamp }}"` | `—` | — |
| 4 | slack-reply | `./slack/send` | `—` | `bot-token`, `channel-id`, `message`, `thread-timestamp` |
| 5 | validate thread-timestamp | `test -n "${{ steps.slack-reply.outputs.thread-timestamp }}"` | `—` | — |
| 6 | slack-multi | `./slack/send` | `—` | `bot-token`, `channel-id`, `thread-timestamp`, `message` |
| 7 | slack-multi-with-double-quotes | `./slack/send` | `—` | `bot-token`, `channel-id`, `thread-timestamp`, `message` |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read`; job overrides: `none`. |
| Local actions | [`slack/send/action.yml`](../../../slack/send/action.yml); [usage README](../../../slack/send/README.md) — This is an opinionated GitHub Action to send a message in slack. Inputs: `bot-token`, `channel-id`, `message`, `thread-timestamp`. Declared outputs: `thread-timestamp`. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `thread-timestamp`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | `SLACK_BOT_TOKEN` |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-slack-send.yml`](../test-slack-send.yml#L1-72)
- Local action: [`slack/send/action.yml`](../../../slack/send/action.yml) and [`slack/send/README.md`](../../../slack/send/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
