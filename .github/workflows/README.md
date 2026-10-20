# GitHub Actions workflow documentation

This index covers every checked-in workflow in [`.github/workflows/`](.). These pages describe repository sources; remote action and reusable-workflow implementations are identified as external where they cannot be verified here.

| Workflow | Documentation |
| --- | --- |
| [`create-major-tag`](./create-major-tag.yml) | [`create-major-tag.md`](docs/create-major-tag.md) |
| [`no-test`](./no-test.yml) | [`no-test.md`](docs/no-test.md) |
| [`pre-commit`](./pre-commit.yml) | [`pre-commit.md`](docs/pre-commit.md) |
| [`release-drafter`](./release-drafter.yml) | [`release-drafter.md`](docs/release-drafter.md) |
| [`required-labels`](./required-labels.yml) | [`required-labels.md`](docs/required-labels.md) |
| [`test-aws-auth`](./test-aws-auth.yml) | [`test-aws-auth.md`](docs/test-aws-auth.md) |
| [`test-azure-auth`](./test-azure-auth.yml) | [`test-azure-auth.md`](docs/test-azure-auth.md) |
| [`test-buildkite-download-artifact`](./test-buildkite-download-artifact.yml) | [`test-buildkite-download-artifact.md`](docs/test-buildkite-download-artifact.md) |
| [`test-buildkite-flaky-report`](./test-buildkite-flaky-report.yml) | [`test-buildkite-flaky-report.md`](docs/test-buildkite-flaky-report.md) |
| [`test-buildkite-run`](./test-buildkite-run.yml) | [`test-buildkite-run.md`](docs/test-buildkite-run.md) |
| [`test-check-dependent-jobs`](./test-check-dependent-jobs.yml) | [`test-check-dependent-jobs.md`](docs/test-check-dependent-jobs.md) |
| [`test-download-kibana-dashboard`](./test-download-kibana-dashboard.yml) | [`test-download-kibana-dashboard.md`](docs/test-download-kibana-dashboard.md) |
| [`test-edot-release-draft-release-notes`](./test-edot-release-draft-release-notes.yml) | [`test-edot-release-draft-release-notes.md`](docs/test-edot-release-draft-release-notes.md) |
| [`test-edot-release-finalize`](./test-edot-release-finalize.yml) | [`test-edot-release-finalize.md`](docs/test-edot-release-finalize.md) |
| [`test-edot-release-pr-range`](./test-edot-release-pr-range.yml) | [`test-edot-release-pr-range.md`](docs/test-edot-release-pr-range.md) |
| [`test-edot-release-prepare-finish`](./test-edot-release-prepare-finish.yml) | [`test-edot-release-prepare-finish.md`](docs/test-edot-release-prepare-finish.md) |
| [`test-edot-release-prepare-start`](./test-edot-release-prepare-start.yml) | [`test-edot-release-prepare-start.md`](docs/test-edot-release-prepare-start.md) |
| [`test-edot-release-publish-guard`](./test-edot-release-publish-guard.yml) | [`test-edot-release-publish-guard.md`](docs/test-edot-release-publish-guard.md) |
| [`test-edot-release-render-release-notes`](./test-edot-release-render-release-notes.yml) | [`test-edot-release-render-release-notes.md`](docs/test-edot-release-render-release-notes.md) |
| [`test-edot-release-start-patch`](./test-edot-release-start-patch.yml) | [`test-edot-release-start-patch.md`](docs/test-edot-release-start-patch.md) |
| [`test-edot-release-version`](./test-edot-release-version.yml) | [`test-edot-release-version.md`](docs/test-edot-release-version.md) |
| [`test-elastic-active-branches`](./test-elastic-active-branches.yml) | [`test-elastic-active-branches.md`](docs/test-elastic-active-branches.md) |
| [`test-elastic-github-commands`](./test-elastic-github-commands.yml) | [`test-elastic-github-commands.md`](docs/test-elastic-github-commands.md) |
| [`test-elastic-gscm-secrets`](./test-elastic-gscm-secrets.yml) | [`test-elastic-gscm-secrets.md`](docs/test-elastic-gscm-secrets.md) |
| [`test-elastic-validate-catalog`](./test-elastic-validate-catalog.yml) | [`test-elastic-validate-catalog.md`](docs/test-elastic-validate-catalog.md) |
| [`test-feature-freeze`](./test-feature-freeze.yml) | [`test-feature-freeze.md`](docs/test-feature-freeze.md) |
| [`test-git-setup`](./test-git-setup.yml) | [`test-git-setup.md`](docs/test-git-setup.md) |
| [`test-github-backport-active`](./test-github-backport-active.yml) | [`test-github-backport-active.md`](docs/test-github-backport-active.md) |
| [`test-github-changed-files`](./test-github-changed-files.yml) | [`test-github-changed-files.md`](docs/test-github-changed-files.md) |
| [`test-github-comment-reaction`](./test-github-comment-reaction.yml) | [`test-github-comment-reaction.md`](docs/test-github-comment-reaction.md) |
| [`test-github-create-token`](./test-github-create-token.yml) | [`test-github-create-token.md`](docs/test-github-create-token.md) |
| [`test-github-is-member-of`](./test-github-is-member-of.yml) | [`test-github-is-member-of.md`](docs/test-github-is-member-of.md) |
| [`test-github-is-pr-author-member-of`](./test-github-is-pr-author-member-of.yml) | [`test-github-is-pr-author-member-of.md`](docs/test-github-is-pr-author-member-of.md) |
| [`test-github-mutex`](./test-github-mutex.yml) | [`test-github-mutex.md`](docs/test-github-mutex.md) |
| [`test-github-project-add`](./test-github-project-add.yml) | [`test-github-project-add.md`](docs/test-github-project-add.md) |
| [`test-github-project-field-set`](./test-github-project-field-set.yml) | [`test-github-project-field-set.md`](docs/test-github-project-field-set.md) |
| [`test-github-user-type`](./test-github-user-type.yml) | [`test-github-user-type.md`](docs/test-github-user-type.md) |
| [`test-google-auth`](./test-google-auth.yml) | [`test-google-auth.md`](docs/test-google-auth.md) |
| [`test-kibana-docker-image`](./test-kibana-docker-image.yml) | [`test-kibana-docker-image.md`](docs/test-kibana-docker-image.md) |
| [`test-maven-await-artifact`](./test-maven-await-artifact.yml) | [`test-maven-await-artifact.md`](docs/test-maven-await-artifact.md) |
| [`test-mergify-labels-copier`](./test-mergify-labels-copier.yml) | [`test-mergify-labels-copier.md`](docs/test-mergify-labels-copier.md) |
| [`test-oblt-cli-cluster-create-ccs`](./test-oblt-cli-cluster-create-ccs.yml) | [`test-oblt-cli-cluster-create-ccs.md`](docs/test-oblt-cli-cluster-create-ccs.md) |
| [`test-oblt-cli-cluster-create-custom`](./test-oblt-cli-cluster-create-custom.yml) | [`test-oblt-cli-cluster-create-custom.md`](docs/test-oblt-cli-cluster-create-custom.md) |
| [`test-oblt-cli-cluster-create-serverless`](./test-oblt-cli-cluster-create-serverless.yml) | [`test-oblt-cli-cluster-create-serverless.md`](docs/test-oblt-cli-cluster-create-serverless.md) |
| [`test-oblt-cli-cluster-credentials`](./test-oblt-cli-cluster-credentials.yml) | [`test-oblt-cli-cluster-credentials.md`](docs/test-oblt-cli-cluster-credentials.md) |
| [`test-oblt-cli-cluster-name-validation`](./test-oblt-cli-cluster-name-validation.yml) | [`test-oblt-cli-cluster-name-validation.md`](docs/test-oblt-cli-cluster-name-validation.md) |
| [`test-deploy-my-kibana`](./test-oblt-cli-deploy-my-kibana.yml) | [`test-oblt-cli-deploy-my-kibana.md`](docs/test-oblt-cli-deploy-my-kibana.md) |
| [`test-oblt-cli-list`](./test-oblt-cli-list.yml) | [`test-oblt-cli-list.md`](docs/test-oblt-cli-list.md) |
| [`test-oblt-cli-run`](./test-oblt-cli-run.yml) | [`test-oblt-cli-run.md`](docs/test-oblt-cli-run.md) |
| [`test-oblt-cli-setup`](./test-oblt-cli-setup.yml) | [`test-oblt-cli-setup.md`](docs/test-oblt-cli-setup.md) |
| [`test-undeploy-my-kibana`](./test-oblt-cli-undeploy-my-kibana.yml) | [`test-oblt-cli-undeploy-my-kibana.md`](docs/test-oblt-cli-undeploy-my-kibana.md) |
| [`test-pre-commit`](./test-pre-commit.yml) | [`test-pre-commit.md`](docs/test-pre-commit.md) |
| [`test-slack-notify-result`](./test-slack-notify-result.yml) | [`test-slack-notify-result.md`](docs/test-slack-notify-result.md) |
| [`test-slack-send`](./test-slack-send.yml) | [`test-slack-send.md`](docs/test-slack-send.md) |
| [`test-updatecli-install`](./test-updatecli-install.yml) | [`test-updatecli-install.md`](docs/test-updatecli-install.md) |
| [`test-updatecli-run`](./test-updatecli-run.yml) | [`test-updatecli-run.md`](docs/test-updatecli-run.md) |
| [`test-version-framework`](./test-version-framework.yml) | [`test-version-framework.md`](docs/test-version-framework.md) |
| [`Observability Agentic Workflow — Issue Comment`](./trigger-obs-aw-issue-comment.yml) | [`trigger-obs-aw-issue-comment.md`](docs/trigger-obs-aw-issue-comment.md) |
| [`Observability Agentic Workflow — Issues`](./trigger-obs-aw-issues.yml) | [`trigger-obs-aw-issues.md`](docs/trigger-obs-aw-issues.md) |
| [`Observability Agentic Workflow — Pull Request`](./trigger-obs-aw-pull-request.yml) | [`trigger-obs-aw-pull-request.md`](docs/trigger-obs-aw-pull-request.md) |
| [`Observability Agentic Workflow — Schedule (daily)`](./trigger-obs-aw-schedule-daily.yml) | [`trigger-obs-aw-schedule-daily.md`](docs/trigger-obs-aw-schedule-daily.md) |
| [`Observability Agentic Workflow — Schedule (frequent)`](./trigger-obs-aw-schedule-frequent.yml) | [`trigger-obs-aw-schedule-frequent.md`](docs/trigger-obs-aw-schedule-frequent.md) |
| [`Observability Agentic Workflow — Status`](./trigger-obs-aw-status.yml) | [`trigger-obs-aw-status.md`](docs/trigger-obs-aw-status.md) |
| [`updatecli`](./updatecli.yml) | [`updatecli.md`](docs/updatecli.md) |

## Source coverage

The existing root README mentions legacy `trigger-oblt-aw-*` filenames; the checked-in workflows currently use `trigger-obs-aw-*`. This inventory follows the checked-in sources.

The repository contains no checked-in Buildkite pipeline YAML/configuration, and the read-only Buildkite lookup for `elastic/oblt-actions` returned no matching remote pipeline. The `buildkite/` directory contains GitHub composite actions, not pipeline definitions; their usage is documented in the action READMEs.
