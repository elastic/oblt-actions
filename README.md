# GitHub Actions for Elastic Observability projects

[![GitHub release](https://img.shields.io/github/release/elastic/oblt-actions.svg?label=release&logo=github)](https://github.com/elastic/oblt-actions/releases/latest)

This repository contains GitHub Actions for Elastic Observability projects.

## Actions catalog

The repository is organized by action namespace. Each action directory contains its own `action.yml` and usage README.

| Namespace | Action docs |
| --- | --- |
| `aws/` | [`auth`](aws/auth/README.md) |
| `azure/` | [`auth`](azure/auth/README.md) |
| `buildkite/` | [`download-artifact`](buildkite/download-artifact/README.md), [`flaky-report`](buildkite/flaky-report/README.md), [`run`](buildkite/run/README.md) |
| `check-dependent-jobs/` | [`check-dependent-jobs`](check-dependent-jobs/README.md) |
| `download-kibana-dashboard/` | [`download-kibana-dashboard`](download-kibana-dashboard/README.md) |
| `elastic/` | [`active-branches`](elastic/active-branches/README.md), [`github-commands`](elastic/github-commands/README.md), [`validate-catalog`](elastic/validate-catalog/README.md) |
| `feature-freeze/` | [`feature-freeze`](feature-freeze/README.md) |
| `git/` | [`setup`](git/setup/README.md) |
| `github/` | [`backport-active`](github/backport-active/README.md), [`changed-files`](github/changed-files/README.md), [`comment-reaction`](github/comment-reaction/README.md), [`create-token`](github/create-token/README.md), [`is-member-of`](github/is-member-of/README.md), [`is-pr-author-member-of`](github/is-pr-author-member-of/README.md), [`mutex`](github/mutex/README.md), [`project-add`](github/project-add/README.md), [`project-field-set`](github/project-field-set/README.md), [`user-type`](github/user-type/README.md), [`validate-comment`](github/validate-comment/README.md) |
| `google/` | [`auth`](google/auth/README.md) |
| `kibana-docker-image/` | [`kibana-docker-image`](kibana-docker-image/README.md) |
| `maven/` | [`await-artifact`](maven/await-artifact/README.md) |
| `mergify/` | [`labels-copier`](mergify/labels-copier/README.md) |
| `oblt-cli/` | [`cluster-credentials`](oblt-cli/cluster-credentials/README.md), [`cluster-create-ccs`](oblt-cli/cluster-create-ccs/README.md), [`cluster-create-custom`](oblt-cli/cluster-create-custom/README.md), [`cluster-create-serverless`](oblt-cli/cluster-create-serverless/README.md), [`cluster-destroy`](oblt-cli/cluster-destroy/README.md), [`cluster-name-validation`](oblt-cli/cluster-name-validation/README.md), [`deploy-my-kibana`](oblt-cli/deploy-my-kibana/README.md), [`list`](oblt-cli/list/README.md), [`run`](oblt-cli/run/README.md), [`setup`](oblt-cli/setup/README.md), [`undeploy-my-kibana`](oblt-cli/undeploy-my-kibana/README.md) |
| `pre-commit/` | [`pre-commit`](pre-commit/README.md) |
| `slack/` | [`notify-result`](slack/notify-result/README.md), [`send`](slack/send/README.md) |
| `snapshoty/` | [`run`](snapshoty/run/README.md) |
| `test-report/` | [`test-report`](test-report/README.md) |
| `updatecli/` | [`install`](updatecli/install/README.md), [`run`](updatecli/run/README.md), [`run-and-notify`](updatecli/run-and-notify/README.md) |
| `version-framework/` | [`version-framework`](version-framework/README.md) |

## Automation workflows

### Observability Agentic Workflow Triggers

The repository uses multiple `.github/workflows/trigger-oblt-aw-*.yml` workflows to forward scoped repository events to reusable workflows in `elastic/oblt-aw`.

Current trigger workflows include:
- `.github/workflows/trigger-oblt-aw-autodoc.yml`
- `.github/workflows/trigger-oblt-aw-issue-triage.yml`
- `.github/workflows/trigger-oblt-aw-issue-fixer.yml`
- `.github/workflows/trigger-oblt-aw-mention-in-issue.yml`
- `.github/workflows/trigger-oblt-aw-automerge.yml`
- `.github/workflows/trigger-oblt-aw-dependency-review.yml`
- `.github/workflows/trigger-oblt-aw-duplicate-issue-detector.yml`
- `.github/workflows/trigger-oblt-aw-resource-not-accessible-by-integration-detector.yml`
- `.github/workflows/trigger-oblt-aw-resource-not-accessible-by-integration-triage.yml`
- `.github/workflows/trigger-oblt-aw-resource-not-accessible-by-integration-fixer.yml`
- `.github/workflows/trigger-oblt-aw-security-detector.yml`
- `.github/workflows/trigger-oblt-aw-security-triage.yml`
- `.github/workflows/trigger-oblt-aw-security-fixer.yml`
- `.github/workflows/trigger-oblt-aw-agent-suggestions.yml`
- `.github/workflows/trigger-oblt-aw-estc-pr-buildkite-detective.yml`

Secret forwarding currently works as follows:
- Most trigger workflows pass `COPILOT_GITHUB_TOKEN` through as `COPILOT_GITHUB_TOKEN`.
- `.github/workflows/trigger-oblt-aw-estc-pr-buildkite-detective.yml` additionally passes `BUILDKITE_LOGS_API_TOKEN` as `BUILDKITE_API_TOKEN` for Buildkite log triage.

### Kibana deploy/undeploy side effects

The `oblt-cli/deploy-my-kibana` and `oblt-cli/undeploy-my-kibana` actions create issues in `elastic/observability-test-environments`:

- `deploy-my-kibana` creates an issue labeled `deploy-custom-kibana`
- `undeploy-my-kibana` creates an issue labeled `destroy-custom-kibana-serverless`

When using these actions, provide credentials with `issues: write` permission on `elastic/observability-test-environments`.

### updatecli automation

The repository includes the `.github/workflows/updatecli.yml` workflow, which runs Updatecli compose automation against `oblt-actions` and `observability-test-environments`.

It runs on:
- a weekly schedule (`0 6 * * 6`)
- manual dispatch (`workflow_dispatch`)

This workflow requires the repository secrets `OBS_AUTOMATION_APP_ID` and `OBS_AUTOMATION_APP_PEM` to generate a GitHub App token with write access to contents and pull requests for the target repositories.

## Releasing

See [RELEASE.md](docs/RELEASE.md) for the release process.

<sup><br>Made with ♥️ and ☕️ by Elastic and our community.</sup>
