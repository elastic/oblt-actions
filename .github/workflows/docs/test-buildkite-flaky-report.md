# test-buildkite-flaky-report

Test workflow for `buildkite-flaky-report`. Detects flaky tests from Buildkite Test Engine and creates/updates GitHub issues

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-buildkite-flaky-report.yml`](../test-buildkite-flaky-report.yml#L1-L76) |
| Trigger | `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/test-buildkite-flaky-report.yml, buildkite/flaky-report/**`); `push` (branches: `main`; paths: `.github/workflows/test-buildkite-flaky-report.yml, buildkite/flaky-report/**`) |

## Purpose

Test workflow for `buildkite-flaky-report`. Detects flaky tests from Buildkite Test Engine and creates/updates GitHub issues

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/test-buildkite-flaky-report.yml, buildkite/flaky-report/**`); `push` (branches: `main`; paths: `.github/workflows/test-buildkite-flaky-report.yml, buildkite/flaky-report/**`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-slim` | test-max-issues-0, pytest | `always()` | `—` |
| `test-max-issues-0` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `pytest` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | check | `elastic/oblt-actions/check-dependent-jobs@v1` | `—` | `jobs` |
| 2 | Step 2 | `${{ steps.check.outputs.is-success }}` | `—` | — |

### `test-max-issues-0` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | buildkite | `./buildkite/flaky-report` | `—` | `github-repo`, `github-token`, `days`, `max-issues`, `org`, `test-suite-id`, `token` |
| 3 | Assert flaky-test-count is 0 | `test "${{ steps.buildkite.outputs.flaky-test-count }}" = "0"` | `—` | — |

### `pytest` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Set up Python | `actions/setup-python@v7` | `—` | `python-version` |
| 3 | Install dependencies | `python -m pip install --upgrade pip pip install requests pytest` | `—` | — |
| 4 | Run pytest | `pytest buildkite/flaky-report/buildkite_flaky_report_tests.py` | `—` | — |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read`; job overrides: `test-max-issues-0: contents: read; pytest: contents: read`. |
| Local actions | [`buildkite/flaky-report/action.yml`](../../../buildkite/flaky-report/action.yml); [usage README](../../../buildkite/flaky-report/README.md) — Detects flaky tests from Buildkite Test Engine and creates/updates GitHub issues Inputs: `token`, `org`, `test-suite-id`, `github-repo`, `github-token`, `github-issue-title-prefix`, `github-label`, `branch`, `days`, `output-dir`, `max-issues`, `endpoint`, `max-runs`, `debug`, `python-version`. Declared outputs: `flaky-test-count`. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `flaky-test-count, is-success`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | `BUILDKITE_TEST_SUITE_TOKEN`, `GITHUB_TOKEN` |

## Local scripts and sources

- [`buildkite/flaky-report/buildkite_flaky_report.py`](../../../buildkite/flaky-report/buildkite_flaky_report.py)
- [`buildkite/flaky-report/buildkite_flaky_report_tests.py`](../../../buildkite/flaky-report/buildkite_flaky_report_tests.py)

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-buildkite-flaky-report.yml`](../test-buildkite-flaky-report.yml#L1-76)
- Local action: [`buildkite/flaky-report/action.yml`](../../../buildkite/flaky-report/action.yml) and [`buildkite/flaky-report/README.md`](../../../buildkite/flaky-report/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
