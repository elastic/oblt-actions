# test-edot-release-prepare-finish

Test workflow for `edot-release-prepare-finish`. Check an EDOT release dispatch, derive the release, and write the version file, applies_to entries, and release-notes section into the working tree. The caller must check out full history and tags.

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-edot-release-prepare-finish.yml`](../test-edot-release-prepare-finish.yml#L1-L335) |
| Trigger | `merge_group`; `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-edot-release-prepare-finish.yml, edot-release/prepare-finish/**, edot-release/prepare-start/**, edot-release/version/**, edot-release/pr-range/**, edot-release/render-release-notes/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-edot-release-prepare-finish.yml, edot-release/prepare-finish/**, edot-release/prepare-start/**, edot-release/version/**, edot-release/pr-range/**, edot-release/render-release-notes/**`) |

## Purpose

Test workflow for `edot-release-prepare-finish`. Check an EDOT release dispatch, derive the release, and write the version file, applies_to entries, and release-notes section into the working tree. The caller must check out full history and tags.

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-edot-release-prepare-finish.yml, edot-release/prepare-finish/**, edot-release/prepare-start/**, edot-release/version/**, edot-release/pr-range/**, edot-release/render-release-notes/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-edot-release-prepare-finish.yml, edot-release/prepare-finish/**, edot-release/prepare-start/**, edot-release/version/**, edot-release/pr-range/**, edot-release/render-release-notes/**`). Conditions below can further restrict individual jobs or steps.

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
| 1 | Step 1 | `actions/checkout@v7` | `—` | `path` |
| 2 | Read release-note fixtures | `data=oblt-actions/edot-release/render-release-notes/test-data { echo "minor=$(jq -c . "$data/android-1.10.0.json")" echo "major=$(jq -c . "$data/ios-sample.json")" } >> "$GITHUB_OUTPUT"` | `—` | — |
| 3 | Create main fixture | `"$FIXTURE" create android 98.1.0-SNAPSHOT v98.0.0 4967b69e2f83588d572e721c4f34928b51ab003e` | `—` | — |
| 4 | start-main | `./oblt-actions/edot-release/prepare-start` | `—` | `notes`, `ref`, `ref-name`, `repository` |
| 5 | Add a generated file | `mkdir -p module echo generated > module/generated.txt "$FIXTURE" snapshot` | `—` | — |
| 6 | finish-main | `./oblt-actions/edot-release/prepare-finish` | `—` | `release`, `ref`, `dry-run`, `repository` |
| 7 | Verify main dry-run | `test -z "$PULL_REQUEST_URL" "$FIXTURE" check-unchanged log="$RUNNER_TEMP/finish-main.log" oblt-actions/edot-release/prepare-finish/prepare-finish.sh > "$log" cat "$log" "$FIXTURE" check-unchanged grep -Fx 'Would run: gi…` | `—` | `PULL_REQUEST_URL`, `RELEASE_JSON`, `RELEASE_REF`, `DRY_RUN`, `RELEASE_REPOSITORY`, `GH_TOKEN` |
| 8 | Create patch fixture | `"$FIXTURE" create android 99.0.0 v99.0.0 4967b69e2f83588d572e721c4f34928b51ab003e` | `—` | — |
| 9 | start-patch | `./oblt-actions/edot-release/prepare-start` | `—` | `notes`, `ref`, `ref-name`, `repository` |
| 10 | Add a generated file | `mkdir -p module echo generated > module/generated.txt "$FIXTURE" snapshot` | `—` | — |
| 11 | finish-patch | `./oblt-actions/edot-release/prepare-finish` | `—` | `release`, `ref`, `dry-run`, `repository` |
| 12 | Verify patch dry-run | `test -z "$PULL_REQUEST_URL" "$FIXTURE" check-unchanged log="$RUNNER_TEMP/finish-patch.log" oblt-actions/edot-release/prepare-finish/prepare-finish.sh > "$log" cat "$log" "$FIXTURE" check-unchanged grep -Fx 'Would run: g…` | `—` | `PULL_REQUEST_URL`, `RELEASE_JSON`, `RELEASE_REF`, `DRY_RUN`, `RELEASE_REPOSITORY`, `GH_TOKEN` |
| 13 | Verify nothing was created on GitHub | `"$FIXTURE" check-upstream elastic/oblt-actions 99.0.0 99.0.1` | `—` | `GH_TOKEN` |

### `invalid` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | `path` |
| 2 | Read release-note fixtures | `echo "major=$(jq -c . oblt-actions/edot-release/render-release-notes/test-data/ios-sample.json)" >> "$GITHUB_OUTPUT"` | `—` | — |
| 3 | Create fixture | `"$FIXTURE" create android 98.1.0-SNAPSHOT v98.0.0 4967b69e2f83588d572e721c4f34928b51ab003e` | `—` | — |
| 4 | short-version | `./oblt-actions/edot-release/prepare-finish` | `—` | `release`, `ref`, `dry-run`, `repository` |
| 5 | Step 5 | `exit 1` | `steps.short-version.outcome != 'failure'` | — |
| 6 | Step 6 | `"$FIXTURE" check-unchanged` | `—` | — |
| 7 | unknown-bump | `./oblt-actions/edot-release/prepare-finish` | `—` | `release`, `ref`, `dry-run`, `repository` |
| 8 | Step 8 | `exit 1` | `steps.unknown-bump.outcome != 'failure'` | — |
| 9 | Step 9 | `"$FIXTURE" check-unchanged` | `—` | — |
| 10 | Create fixture whose run has no Git identity | `"$FIXTURE" create android 98.1.0-SNAPSHOT v98.0.0 4967b69e2f83588d572e721c4f34928b51ab003e` | `—` | — |
| 11 | start-no-identity | `./oblt-actions/edot-release/prepare-start` | `—` | `notes`, `ref`, `ref-name`, `repository` |
| 12 | Add a generated file and remove the Git identity | `mkdir -p module echo generated > module/generated.txt "$FIXTURE" forget-identity "$FIXTURE" snapshot` | `—` | — |
| 13 | no-identity | `./oblt-actions/edot-release/prepare-finish` | `—` | `release`, `ref`, `repository`; `GIT_CONFIG_GLOBAL` |
| 14 | Step 14 | `exit 1` | `steps.no-identity.outcome != 'failure'` | — |
| 15 | Step 15 | `"$FIXTURE" check-origin` | `—` | — |
| 16 | Create fixture with a leftover prepare branch | `"$FIXTURE" create android 98.1.0-SNAPSHOT v98.0.0 4967b69e2f83588d572e721c4f34928b51ab003e leftover=$(git commit-tree -m 'Leftover preparation' 'HEAD^{tree}') git push --quiet origin "$leftover:refs/heads/prepare/99.0.0"` | `—` | — |
| 17 | start-leftover | `./oblt-actions/edot-release/prepare-start` | `—` | `notes`, `ref`, `ref-name`, `repository` |
| 18 | Add a generated file | `mkdir -p module echo generated > module/generated.txt "$FIXTURE" snapshot` | `—` | — |
| 19 | leftover-prepare | `./oblt-actions/edot-release/prepare-finish` | `—` | `release`, `ref`, `repository` |
| 20 | Step 20 | `exit 1` | `steps.leftover-prepare.outcome != 'failure'` | — |
| 21 | Step 21 | `"$FIXTURE" check-origin` | `—` | — |
| 22 | Create fixture whose pull request cannot be opened | `"$FIXTURE" create android 98.1.0-SNAPSHOT v98.0.0 4967b69e2f83588d572e721c4f34928b51ab003e` | `—` | — |
| 23 | start-no-pr | `./oblt-actions/edot-release/prepare-start` | `—` | `notes`, `ref`, `ref-name`, `repository` |
| 24 | Verify a failed pull request deletes the pushed branches | `mkdir -p module echo generated > module/generated.txt "$FIXTURE" snapshot mkdir "$RUNNER_TEMP/failing-gh" printf '#!/bin/sh\nexit 1\n' > "$RUNNER_TEMP/failing-gh/gh" chmod +x "$RUNNER_TEMP/failing-gh/gh" log="$RUNNER_TE…` | `—` | `RELEASE_JSON`, `RELEASE_REF`, `RELEASE_REPOSITORY`, `GH_TOKEN` |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read, pull-requests: read`; job overrides: `none`. |
| Local actions | [`edot-release/prepare-start/action.yml`](../../../edot-release/prepare-start/action.yml); [usage README](../../../edot-release/prepare-start/README.md) (called as `./oblt-actions/edot-release/prepare-start`); checked out under `path: oblt-actions` — Check an EDOT release dispatch, derive the release, and write the version file, applies_to entries, and release-notes section into the working tree. The caller must check out full history and tags. Inputs: `notes`, `ref`, `ref-name`, `repository`, `github-token`. Declared outputs: `prepared`, `version`, `previous-tag`, `release`.<br>[`edot-release/prepare-finish/action.yml`](../../../edot-release/prepare-finish/action.yml); [usage README](../../../edot-release/prepare-finish/README.md) (called as `./oblt-actions/edot-release/prepare-finish`); checked out under `path: oblt-actions` — Push the EDOT release branches and open the preparation pull request for the release changes in the working tree. Inputs: `release`, `ref`, `dry-run`, `repository`, `github-token`. Declared outputs: `pull-request-url`. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `is-success, major, minor, pull-request-url, release`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | No `secrets.*` references found in the workflow source. |

## Local scripts and sources

- [`edot-release/prepare-start/prepare-start.sh`](../../../edot-release/prepare-start/prepare-start.sh)
- [`edot-release/prepare-finish/prepare-finish.sh`](../../../edot-release/prepare-finish/prepare-finish.sh)
- [`edot-release/prepare-start/test-data/fixture.sh`](../../../edot-release/prepare-start/test-data/fixture.sh)

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-edot-release-prepare-finish.yml`](../test-edot-release-prepare-finish.yml#L1-335)
- Local action: [`edot-release/prepare-start/action.yml`](../../../edot-release/prepare-start/action.yml) and [`edot-release/prepare-start/README.md`](../../../edot-release/prepare-start/README.md)
- Local action: [`edot-release/prepare-finish/action.yml`](../../../edot-release/prepare-finish/action.yml) and [`edot-release/prepare-finish/README.md`](../../../edot-release/prepare-finish/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
