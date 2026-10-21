# test-feature-freeze

Test workflow for `feature-freeze`. An Action to check if a repository is currently in a feature freeze period.

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-feature-freeze.yml`](../test-feature-freeze.yml#L1-L99) |
| Trigger | `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/test-feature-freeze.yml, feature-freeze/**`); `push` (branches: `main`; paths: `.github/workflows/test-feature-freeze.yml, feature-freeze/**`) |

## Purpose

Test workflow for `feature-freeze`. An Action to check if a repository is currently in a feature freeze period.

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `pull_request` (branches: `main`; paths: `.github/workflows/test-feature-freeze.yml, feature-freeze/**`); `push` (branches: `main`; paths: `.github/workflows/test-feature-freeze.yml, feature-freeze/**`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-slim` | test-freeze-detection, test-no-freeze | `Default GitHub condition` | `—` |
| `test-freeze-detection` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `test-no-freeze` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | check | `elastic/oblt-actions/check-dependent-jobs@v1` | `—` | `jobs` |
| 2 | Step 2 | `${{ steps.check.outputs.is-success }}` | `—` | — |

### `test-freeze-detection` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Setup release-freezes.json | `if date -v +1d >/dev/null 2>&1; then # macOS TOMORROW=$(date -v +1d +%Y-%m-%d) else # Linux TOMORROW=$(date -d tomorrow +%Y-%m-%d) fi FILE="${RUNNER_TEMP}/release-freezes.json" cat <<EOF > "$FILE" [ { "begin": "2025-11-…` | `—` | — |
| 3 | feature-freeze | `./feature-freeze` | `—` | `feature-freeze-file` |
| 4 | validate feature freeze is active | `test "${{steps.feature-freeze.outputs.in-freeze}}" = "true"` | `—` | — |

### `test-no-freeze` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Setup my-release-freezes.json | `FILE="${RUNNER_TEMP}/my-release-freezes.json" cat <<EOF > "$FILE" [ { "begin": "2023-12-23", "end": "2024-12-23", "description": "EOY Holiday Season" } ] EOF echo "freeze-file=${FILE}" >> "$GITHUB_OUTPUT" cat "$FILE"` | `—` | — |
| 3 | feature-freeze | `./feature-freeze` | `—` | `feature-freeze-file` |
| 4 | validate feature freeze is not active | `test "${{steps.feature-freeze.outputs.in-freeze}}" = "false"` | `—` | — |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read`; job overrides: `none`. |
| Local actions | [`feature-freeze/action.yml`](../../../feature-freeze/action.yml); [usage README](../../../feature-freeze/README.md) — An Action to check if a repository is currently in a feature freeze period. Inputs: `github-repository`, `git-ref`, `feature-freeze-file`. Declared outputs: `in-freeze`. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `freeze-file, in-freeze, is-success`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | No `secrets.*` references found in the workflow source. |

## Local scripts and sources

- [`feature-freeze/check-release-freeze.sh`](../../../feature-freeze/check-release-freeze.sh)

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-feature-freeze.yml`](../test-feature-freeze.yml#L1-99)
- Local action: [`feature-freeze/action.yml`](../../../feature-freeze/action.yml) and [`feature-freeze/README.md`](../../../feature-freeze/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
