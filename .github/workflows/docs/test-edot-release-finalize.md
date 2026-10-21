# test-edot-release-finalize

Test workflow for `edot-release-finalize`. Create the EDOT release tag and GitHub Release, then open the release pull request into main, or the release-notes pull request for a patch release.

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-edot-release-finalize.yml`](../test-edot-release-finalize.yml#L1-L372) |
| Trigger | `merge_group`; `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-edot-release-finalize.yml, edot-release/finalize/**, edot-release/prepare-start/**, edot-release/version/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-edot-release-finalize.yml, edot-release/finalize/**, edot-release/prepare-start/**, edot-release/version/**`) |

## Purpose

Test workflow for `edot-release-finalize`. Create the EDOT release tag and GitHub Release, then open the release pull request into main, or the release-notes pull request for a patch release.

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-edot-release-finalize.yml, edot-release/finalize/**, edot-release/prepare-start/**, edot-release/version/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-edot-release-finalize.yml, edot-release/finalize/**, edot-release/prepare-start/**, edot-release/version/**`). Conditions below can further restrict individual jobs or steps.

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
| 2 | Create main release fixture | `"$FIXTURE" create android 98.1.0-SNAPSHOT v98.0.0 git switch --quiet -c releasing/99.0.0 "$FIXTURE" set-version 99.0.0 "$FIXTURE" add-section 99.0.0 sha=$("$FIXTURE" commit 'Prepare release 99.0.0') git push --quiet ori…` | `—` | — |
| 3 | main | `./oblt-actions/edot-release/finalize` | `—` | `release`, `dry-run`, `repository` |
| 4 | Verify main dry-run | `test -z "$RELEASE_URL" test -z "$MAIN_PULL_REQUEST_URL" "$FIXTURE" check-unchanged log="$RUNNER_TEMP/main.log" oblt-actions/edot-release/finalize/finalize.sh > "$log" cat "$log" "$FIXTURE" check-unchanged grep -Fx "Woul…` | `—` | `RELEASE_URL`, `MAIN_PULL_REQUEST_URL`, `RELEASE_SHA`, `RELEASE_JSON`, `DRY_RUN`, `RELEASE_REPOSITORY`, `GH_TOKEN` |
| 5 | Create resumed release fixture | `git tag v99.0.0 "$SHA" "$FIXTURE" set-version 99.1.0-SNAPSHOT "$FIXTURE" commit 'Prepare for the next release' > /dev/null git push --quiet origin \ refs/heads/releasing/99.0.0:refs/heads/releasing/99.0.0 \ refs/tags/v9…` | `—` | `SHA` |
| 6 | resumed | `./oblt-actions/edot-release/finalize` | `—` | `release`, `dry-run`, `repository` |
| 7 | Verify resumed dry-run | `test -z "$RELEASE_URL" test -z "$MAIN_PULL_REQUEST_URL" "$FIXTURE" check-unchanged log="$RUNNER_TEMP/resumed.log" oblt-actions/edot-release/finalize/finalize.sh > "$log" cat "$log" "$FIXTURE" check-unchanged if grep -E …` | `—` | `RELEASE_URL`, `MAIN_PULL_REQUEST_URL`, `RELEASE_SHA`, `RELEASE_JSON`, `DRY_RUN`, `RELEASE_REPOSITORY`, `GH_TOKEN` |
| 8 | Create patch release fixture | `"$FIXTURE" create android 98.1.0-SNAPSHOT v98.0.0 "$FIXTURE" set-version 99.0.0 "$FIXTURE" add-section 99.0.0 "$FIXTURE" commit 'Prepare release 99.0.0' > /dev/null git tag v99.0.0 "$FIXTURE" set-version 99.1.0-SNAPSHOT…` | `—` | — |
| 9 | patch | `./oblt-actions/edot-release/finalize` | `—` | `release`, `dry-run`, `repository` |
| 10 | Verify patch dry-run | `test -z "$RELEASE_URL" test -z "$MAIN_PULL_REQUEST_URL" "$FIXTURE" check-unchanged log="$RUNNER_TEMP/patch.log" oblt-actions/edot-release/finalize/finalize.sh > "$log" cat "$log" "$FIXTURE" check-unchanged grep -Fx "Wou…` | `—` | `RELEASE_URL`, `MAIN_PULL_REQUEST_URL`, `RELEASE_SHA`, `RELEASE_JSON`, `DRY_RUN`, `RELEASE_REPOSITORY`, `GH_TOKEN` |
| 11 | Verify nothing was created on GitHub | `"$FIXTURE" check-upstream elastic/oblt-actions 99.0.0 99.0.1` | `—` | `GH_TOKEN` |

### `invalid` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | `path` |
| 2 | Create fixture | `"$FIXTURE" create android 98.1.0-SNAPSHOT v98.0.0 "$FIXTURE" add-section 99.0.1 "$FIXTURE" commit 'Notes for 99.0.1 without their pull request' > /dev/null git switch --quiet -c releasing/99.0.0 v98.0.0 "$FIXTURE" set-v…` | `—` | — |
| 3 | Abbreviate the release commit | `echo "sha=${RELEASE:0:12}" >> "$GITHUB_OUTPUT"` | `—` | `RELEASE` |
| 4 | short-sha | `./oblt-actions/edot-release/finalize` | `—` | `release`, `dry-run`, `repository` |
| 5 | Step 5 | `exit 1` | `steps.short-sha.outcome != 'failure'` | — |
| 6 | Step 6 | `"$FIXTURE" check-unchanged` | `—` | — |
| 7 | short-version | `./oblt-actions/edot-release/finalize` | `—` | `release`, `dry-run`, `repository` |
| 8 | Step 8 | `exit 1` | `steps.short-version.outcome != 'failure'` | — |
| 9 | Step 9 | `"$FIXTURE" check-unchanged` | `—` | — |
| 10 | tag-exists-yes | `./oblt-actions/edot-release/finalize` | `—` | `release`, `dry-run`, `repository` |
| 11 | Step 11 | `exit 1` | `steps.tag-exists-yes.outcome != 'failure'` | — |
| 12 | Step 12 | `"$FIXTURE" check-unchanged` | `—` | — |
| 13 | other-base | `./oblt-actions/edot-release/finalize` | `—` | `release`, `dry-run`, `repository` |
| 14 | Step 14 | `exit 1` | `steps.other-base.outcome != 'failure'` | — |
| 15 | Step 15 | `"$FIXTURE" check-unchanged` | `—` | — |
| 16 | moved-branch | `./oblt-actions/edot-release/finalize` | `—` | `release`, `dry-run`, `repository` |
| 17 | Step 17 | `exit 1` | `steps.moved-branch.outcome != 'failure'` | — |
| 18 | Step 18 | `"$FIXTURE" check-unchanged` | `—` | — |
| 19 | notes-on-main | `./oblt-actions/edot-release/finalize` | `—` | `release`, `dry-run`, `repository` |
| 20 | Step 20 | `exit 1` | `steps.notes-on-main.outcome != 'failure'` | — |
| 21 | Step 21 | `"$FIXTURE" check-unchanged` | `—` | — |
| 22 | failed-pr-lookup | `./oblt-actions/edot-release/finalize` | `—` | `release`, `dry-run`, `repository` |
| 23 | Step 23 | `exit 1` | `steps.failed-pr-lookup.outcome != 'failure'` | — |
| 24 | Step 24 | `"$FIXTURE" check-unchanged` | `—` | — |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read, pull-requests: read`; job overrides: `none`. |
| Local actions | [`edot-release/finalize/action.yml`](../../../edot-release/finalize/action.yml); [usage README](../../../edot-release/finalize/README.md) (called as `./oblt-actions/edot-release/finalize`); checked out under `path: oblt-actions` — Create the EDOT release tag and GitHub Release, then open the release pull request into main, or the release-notes pull request for a patch release. Inputs: `release`, `dry-run`, `repository`, `github-token`. Declared outputs: `release-url`, `main-pull-request-url`. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `is-success, lookup, main-pull-request-url, patch, release, release-url, sha`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | No `secrets.*` references found in the workflow source. |

## Local scripts and sources

- [`edot-release/finalize/finalize.sh`](../../../edot-release/finalize/finalize.sh)
- [`edot-release/prepare-start/test-data/fixture.sh`](../../../edot-release/prepare-start/test-data/fixture.sh)

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-edot-release-finalize.yml`](../test-edot-release-finalize.yml#L1-372)
- Local action: [`edot-release/finalize/action.yml`](../../../edot-release/finalize/action.yml) and [`edot-release/finalize/README.md`](../../../edot-release/finalize/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
