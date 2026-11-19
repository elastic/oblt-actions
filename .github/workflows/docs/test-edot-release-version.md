# test-edot-release-version

Test workflow for `edot-release-version`. Derive EDOT release tags and versions from repository state.

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-edot-release-version.yml`](../test-edot-release-version.yml#L1-L220) |
| Trigger | `merge_group`; `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-edot-release-version.yml, edot-release/version/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-edot-release-version.yml, edot-release/version/**`) |

## Purpose

Test workflow for `edot-release-version`. Derive EDOT release tags and versions from repository state.

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-edot-release-version.yml, edot-release/version/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-edot-release-version.yml, edot-release/version/**`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-slim` | valid, invalid | `always()` | `—` |
| `valid` | `ubuntu-slim` | None declared | `Default GitHub condition` | `—` |
| `invalid` | `ubuntu-slim` | None declared | `Default GitHub condition` | `—` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | check | `elastic/oblt-actions/check-dependent-jobs@v1` | `—` | `jobs` |
| 2 | Step 2 | `${{ steps.check.outputs.is-success }}` | `—` | — |

### `valid` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Create tag fixtures | `for repository in prefixed plain; do git init -q "$RUNNER_TEMP/$repository" git -C "$RUNNER_TEMP/$repository" config user.name test git -C "$RUNNER_TEMP/$repository" config user.email test@example.com touch "$RUNNER_TEM…` | `—` | — |
| 3 | prefixed-highest | `./edot-release/version` | `—` | `command`, `tag-prefix`; `GIT_DIR` |
| 4 | Step 4 | `test '${{ steps.prefixed-highest.outputs.value }}' = v1.10.1` | `—` | — |
| 5 | plain-highest | `./edot-release/version` | `—` | `command`; `GIT_DIR` |
| 6 | Step 6 | `test '${{ steps.plain-highest.outputs.value }}' = 2.1.0` | `—` | — |
| 7 | line-highest | `./edot-release/version` | `—` | `command`, `tag-prefix`, `line`; `GIT_DIR` |
| 8 | Step 8 | `test '${{ steps.line-highest.outputs.value }}' = v1.10.1` | `—` | — |
| 9 | patch-previous | `./edot-release/version` | `—` | `command`, `tag-prefix`, `ref-name`; `GIT_DIR` |
| 10 | Step 10 | `test '${{ steps.patch-previous.outputs.value }}' = v1.10.1` | `—` | — |
| 11 | main-previous | `./edot-release/version` | `—` | `command`, `tag-prefix`, `ref-name`; `GIT_DIR` |
| 12 | Step 12 | `test '${{ steps.main-previous.outputs.value }}' = v1.10.1` | `—` | — |
| 13 | next-patch | `./edot-release/version` | `—` | `command`, `tag-prefix`, `version` |
| 14 | Step 14 | `test '${{ steps.next-patch.outputs.value }}' = 1.10.2` | `—` | — |
| 15 | minor | `./edot-release/version` | `—` | `command`, `tag-prefix`, `previous-tag`, `development-version`, `bump` |
| 16 | Step 16 | `test '${{ steps.minor.outputs.value }}' = 1.11.0` | `—` | — |
| 17 | major | `./edot-release/version` | `—` | `command`, `tag-prefix`, `previous-tag`, `development-version`, `bump` |
| 18 | Step 18 | `test '${{ steps.major.outputs.value }}' = 2.0.0` | `—` | — |
| 19 | next-development | `./edot-release/version` | `—` | `command`, `version` |
| 20 | Step 20 | `test '${{ steps.next-development.outputs.value }}' = 1.12.0-SNAPSHOT` | `—` | — |

### `invalid` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Create rejection fixtures | `for repository in tagged untagged; do git init -q "$RUNNER_TEMP/$repository" git -C "$RUNNER_TEMP/$repository" config user.name test git -C "$RUNNER_TEMP/$repository" config user.email test@example.com touch "$RUNNER_TE…` | `—` | — |
| 3 | wrong-development | `./edot-release/version` | `—` | `command`, `tag-prefix`, `previous-tag`, `development-version`, `bump` |
| 4 | Step 4 | `exit 1` | `steps.wrong-development.outcome != 'failure'` | — |
| 5 | malformed-line | `./edot-release/version` | `—` | `command`, `tag-prefix`, `line`; `GIT_DIR` |
| 6 | Step 6 | `exit 1` | `steps.malformed-line.outcome != 'failure'` | — |
| 7 | zero-patch | `./edot-release/version` | `—` | `command`, `tag-prefix`, `ref-name` |
| 8 | Step 8 | `exit 1` | `steps.zero-patch.outcome != 'failure'` | — |
| 9 | no-matching-tag | `./edot-release/version` | `—` | `command`, `tag-prefix`; `GIT_DIR` |
| 10 | Step 10 | `exit 1` | `steps.no-matching-tag.outcome != 'failure'` | — |
| 11 | leading-zero | `./edot-release/version` | `—` | `command`, `version` |
| 12 | Step 12 | `exit 1` | `steps.leading-zero.outcome != 'failure'` | — |
| 13 | literal-command | `./edot-release/version` | `—` | `command`, `version` |
| 14 | Step 14 | `exit 1` | `steps.literal-command.outcome != 'failure'` | — |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read`; job overrides: `none`. |
| Local actions | [`edot-release/version/action.yml`](../../../edot-release/version/action.yml); [usage README](../../../edot-release/version/README.md) — Derive EDOT release tags and versions from repository state. Inputs: `command`, `tag-prefix`, `line`, `ref-name`, `version`, `previous-tag`, `development-version`, `bump`. Declared outputs: `value`. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `is-success, value`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | No `secrets.*` references found in the workflow source. |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-edot-release-version.yml`](../test-edot-release-version.yml#L1-220)
- Local action: [`edot-release/version/action.yml`](../../../edot-release/version/action.yml) and [`edot-release/version/README.md`](../../../edot-release/version/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
