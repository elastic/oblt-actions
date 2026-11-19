# no-test

Provides a required `test` job for changes without a dedicated action test workflow and handles fork-PR notification.

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`no-test.yml`](../no-test.yml#L1-L66) |
| Trigger | `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `**, !.github/workflows/test-*, !aws/auth/**, !azure/auth/**, !buildkite/flaky-report/**, !buildkite/run/**, !check-dependent-jobs/**, !download-kibana-dashboard/**, !edot-release/**, !elastic/github-commands/**, !elastic/gscm-secrets/**, !elastic/validate-catalog/**, !feature-freeze/**, !git/setup/**, !github/backport-active/**, !github/changed-files/**, !github/create-token/**, !github/project-add/**, !github/project-field-set/**, !github/user-type/**, !google/auth/**, !oblt-cli/cluster-name-validation/**, !oblt-cli/list/**, !oblt-cli/run/**, !pre-commit/**, !updatecli/run/**`) |

## Purpose

Provides a required `test` job for changes without a dedicated action test workflow and handles fork-PR notification.

The contribution guide documents this fallback workflow and the path exclusions that pair with dedicated tests.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `**, !.github/workflows/test-*, !aws/auth/**, !azure/auth/**, !buildkite/flaky-report/**, !buildkite/run/**, !check-dependent-jobs/**, !download-kibana-dashboard/**, !edot-release/**, !elastic/github-commands/**, !elastic/gscm-secrets/**, !elastic/validate-catalog/**, !feature-freeze/**, !git/setup/**, !github/backport-active/**, !github/changed-files/**, !github/create-token/**, !github/project-add/**, !github/project-field-set/**, !github/user-type/**, !google/auth/**, !oblt-cli/cluster-name-validation/**, !oblt-cli/list/**, !oblt-cli/run/**, !pre-commit/**, !updatecli/run/**`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-slim` | None declared | `Default GitHub condition` | `—` |
| `notify-fork` | `ubuntu-slim` | None declared | `github.event_name == 'pull_request' && github.event.pull_request.head.repo.fork == true` | `—` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `echo "No test to run"` | `—` | — |

### `notify-fork` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Warn about fork | `echo "::warning::Fork pull requests cannot run the e2e tests. Create a feature branch in the main repo to run them."` | `—` | — |
| 2 | Notify PR about fork | `edumserrano/find-create-or-update-comment@82880b65c8a3a6e4c70aa05a204995b6c9696f53` | `—` | `issue-number`, `body-includes`, `comment-author`, `edit-mode`, `body` |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read`; job overrides: `notify-fork: pull-requests: write`. |
| Local actions | None. |
| Outputs | No workflow/job outputs are declared. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | No `secrets.*` references found in the workflow source. |

## Operational notes

Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`no-test.yml`](../no-test.yml#L1-66)

- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
