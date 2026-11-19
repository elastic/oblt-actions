# test-edot-release-start-patch

Test workflow for `edot-release-start-patch`. Cut the EDOT patch branch patching/X.Y.Z from the highest release tag of a line and cherry-pick merged main pull requests onto it. The caller checks out full history and tags and configures the Git identity and credentials.

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-edot-release-start-patch.yml`](../test-edot-release-start-patch.yml#L1-L420) |
| Trigger | `merge_group`; `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-edot-release-start-patch.yml, edot-release/start-patch/**, edot-release/prepare-start/**, edot-release/version/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-edot-release-start-patch.yml, edot-release/start-patch/**, edot-release/prepare-start/**, edot-release/version/**`) |

## Purpose

Test workflow for `edot-release-start-patch`. Cut the EDOT patch branch patching/X.Y.Z from the highest release tag of a line and cherry-pick merged main pull requests onto it. The caller checks out full history and tags and configures the Git identity and credentials.

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-edot-release-start-patch.yml, edot-release/start-patch/**, edot-release/prepare-start/**, edot-release/version/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-edot-release-start-patch.yml, edot-release/start-patch/**, edot-release/prepare-start/**, edot-release/version/**`). Conditions below can further restrict individual jobs or steps.

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
| 2 | Create Android fixture | `"$FIXTURE" create android 99.1.0-SNAPSHOT v99.0.0 "$FIXTURE" commit 'Release v99.0.1' > /dev/null git tag v99.0.1 "$FIXTURE" commit 'Release v99.1.0' > /dev/null git tag v99.1.0 git push --quiet origin refs/heads/main:r…` | `—` | — |
| 3 | picks | `./oblt-actions/edot-release/start-patch` | `—` | `line`, `pull-requests`, `ref-name`, `dry-run`, `repository` |
| 4 | Verify picks dry-run | `"$FIXTURE" check-unchanged log="$RUNNER_TEMP/picks.log" "$START_PATCH" > "$log" cat "$log" "$FIXTURE" check-unchanged test "$(grep -c '^Would run:' "$log")" = 1 push=$(grep -Ex 'Would run: git push --force-with-lease=re…` | `—` | `LINE`, `PULL_REQUESTS` |
| 5 | Create iOS fixture | `"$FIXTURE" create ios 99.1.0-SNAPSHOT 99.0.0` | `—` | — |
| 6 | no-picks | `./oblt-actions/edot-release/start-patch` | `—` | `line`, `ref-name`, `dry-run`, `repository` |
| 7 | Verify no-picks dry-run | `"$FIXTURE" check-unchanged log="$RUNNER_TEMP/no-picks.log" "$START_PATCH" > "$log" cat "$log" "$FIXTURE" check-unchanged test "$(grep -c '^Would run:' "$log")" = 1 grep -Fx "Would run: git push --force-with-lease=refs/h…` | `—` | `LINE`, `PULL_REQUESTS` |
| 8 | Verify nothing was created on GitHub | `"$FIXTURE" check-upstream elastic/oblt-actions 99.0.1 99.0.2` | `—` | — |

### `invalid` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | `path` |
| 2 | Create fixture | `"$FIXTURE" create android 99.1.0-SNAPSHOT v99.0.0 "$FIXTURE" commit 'Release v99.0.1' > /dev/null git tag v99.0.1 "$FIXTURE" commit 'Release v99.1.0' > /dev/null git tag v99.1.0 git switch --quiet --detach git rm --quie…` | `—` | — |
| 3 | other-ref | `./oblt-actions/edot-release/start-patch` | `—` | `line`, `ref-name`, `dry-run`, `repository` |
| 4 | Step 4 | `exit 1` | `steps.other-ref.outcome != 'failure'` | — |
| 5 | Step 5 | `"$FIXTURE" check-unchanged if "$START_PATCH" 2> "$RUNNER_TEMP/error.log"; then exit 1; fi cat "$RUNNER_TEMP/error.log" grep -Fx "Start patch runs from main, not 'patching/99.0.2'." "$RUNNER_TEMP/error.log" "$FIXTURE" ch…` | `—` | `LINE`, `RELEASE_REF_NAME` |
| 6 | empty-line | `./oblt-actions/edot-release/start-patch` | `—` | `line`, `ref-name`, `dry-run`, `repository` |
| 7 | Step 7 | `exit 1` | `steps.empty-line.outcome != 'failure'` | — |
| 8 | Step 8 | `"$FIXTURE" check-unchanged if "$START_PATCH" 2> "$RUNNER_TEMP/error.log"; then exit 1; fi cat "$RUNNER_TEMP/error.log" grep -Fx 'line is required; expected X.Y.' "$RUNNER_TEMP/error.log" "$FIXTURE" check-unchanged` | `—` | `LINE` |
| 9 | short-line | `./oblt-actions/edot-release/start-patch` | `—` | `line`, `ref-name`, `dry-run`, `repository` |
| 10 | Step 10 | `exit 1` | `steps.short-line.outcome != 'failure'` | — |
| 11 | Step 11 | `"$FIXTURE" check-unchanged if "$START_PATCH" 2> "$RUNNER_TEMP/error.log"; then exit 1; fi cat "$RUNNER_TEMP/error.log" grep -Fx "Invalid release line '99'; expected X.Y." "$RUNNER_TEMP/error.log" "$FIXTURE" check-unchan…` | `—` | `LINE` |
| 12 | unknown-line | `./oblt-actions/edot-release/start-patch` | `—` | `line`, `ref-name`, `dry-run`, `repository` |
| 13 | Step 13 | `exit 1` | `steps.unknown-line.outcome != 'failure'` | — |
| 14 | Step 14 | `"$FIXTURE" check-unchanged if "$START_PATCH" 2> "$RUNNER_TEMP/error.log"; then exit 1; fi cat "$RUNNER_TEMP/error.log" grep -Fx 'No release exists on line 98.0.' "$RUNNER_TEMP/error.log" "$FIXTURE" check-unchanged` | `—` | `LINE` |
| 15 | manual-release | `./oblt-actions/edot-release/start-patch` | `—` | `line`, `ref-name`, `dry-run`, `repository` |
| 16 | Step 16 | `exit 1` | `steps.manual-release.outcome != 'failure'` | — |
| 17 | Step 17 | `"$FIXTURE" check-unchanged if "$START_PATCH" 2> "$RUNNER_TEMP/error.log"; then exit 1; fi cat "$RUNNER_TEMP/error.log" grep -Fx 'v99.2.0 predates the automated release process; patch this release by hand.' "$RUNNER_TEMP…` | `—` | `LINE` |
| 18 | malformed-pull-request | `./oblt-actions/edot-release/start-patch` | `—` | `line`, `pull-requests`, `ref-name`, `dry-run`, `repository` |
| 19 | Step 19 | `exit 1` | `steps.malformed-pull-request.outcome != 'failure'` | — |
| 20 | Step 20 | `"$FIXTURE" check-unchanged for value in '#527' '527 1137' '527, 1137' '527,' '12a'; do if PULL_REQUESTS=$value "$START_PATCH" 2> "$RUNNER_TEMP/error.log"; then exit 1; fi cat "$RUNNER_TEMP/error.log" grep -Fx "Invalid p…` | `—` | `LINE` |
| 21 | unmerged | `./oblt-actions/edot-release/start-patch` | `—` | `line`, `pull-requests`, `ref-name`, `dry-run`, `repository` |
| 22 | Step 22 | `exit 1` | `steps.unmerged.outcome != 'failure'` | — |
| 23 | Step 23 | `"$FIXTURE" check-unchanged if "$START_PATCH" 2> "$RUNNER_TEMP/error.log"; then exit 1; fi cat "$RUNNER_TEMP/error.log" grep -Fx 'Pull request #1094 must be merged into main in elastic/oblt-actions.' "$RUNNER_TEMP/error.…` | `—` | `LINE`, `PULL_REQUESTS` |
| 24 | other-base | `./oblt-actions/edot-release/start-patch` | `—` | `line`, `pull-requests`, `ref-name`, `dry-run`, `repository` |
| 25 | Step 25 | `exit 1` | `steps.other-base.outcome != 'failure'` | — |
| 26 | Step 26 | `"$FIXTURE" check-unchanged if "$START_PATCH" 2> "$RUNNER_TEMP/error.log"; then exit 1; fi cat "$RUNNER_TEMP/error.log" grep -Fx 'Pull request #472 must be merged into main in elastic/oblt-actions.' "$RUNNER_TEMP/error.l…` | `—` | `LINE`, `PULL_REQUESTS` |
| 27 | two-parents | `./oblt-actions/edot-release/start-patch` | `—` | `line`, `pull-requests`, `ref-name`, `dry-run`, `repository` |
| 28 | Step 28 | `exit 1` | `steps.two-parents.outcome != 'failure'` | — |
| 29 | Step 29 | `"$FIXTURE" check-unchanged if "$START_PATCH" 2> "$RUNNER_TEMP/error.log"; then exit 1; fi cat "$RUNNER_TEMP/error.log" grep -Fx 'Pull request #7 was not squash-merged: its merge commit e20e7f4a0ee426956e0101fe9959b27647…` | `—` | `LINE`, `PULL_REQUESTS`, `RELEASE_REPOSITORY` |
| 30 | conflict | `./oblt-actions/edot-release/start-patch` | `—` | `line`, `pull-requests`, `ref-name`, `dry-run`, `repository` |
| 31 | Step 31 | `exit 1` | `steps.conflict.outcome != 'failure'` | — |
| 32 | Step 32 | `"$FIXTURE" check-unchanged if "$START_PATCH" > "$RUNNER_TEMP/output.log" 2> "$RUNNER_TEMP/error.log"; then exit 1; fi cat "$RUNNER_TEMP/output.log" "$RUNNER_TEMP/error.log" grep -Fx 'Cherry-pick for pull request #1135 c…` | `—` | `LINE`, `PULL_REQUESTS` |
| 33 | repeated | `./oblt-actions/edot-release/start-patch` | `—` | `line`, `pull-requests`, `ref-name`, `dry-run`, `repository` |
| 34 | Step 34 | `exit 1` | `steps.repeated.outcome != 'failure'` | — |
| 35 | Step 35 | `"$FIXTURE" check-unchanged if "$START_PATCH" 2> "$RUNNER_TEMP/error.log"; then exit 1; fi cat "$RUNNER_TEMP/error.log" grep -Fx 'Cherry-pick for pull request #527 conflicted. Dispatch again without #527, then cherry-pic…` | `—` | `LINE`, `PULL_REQUESTS` |
| 36 | Create the patch branch on the fixture origin | `git push --quiet origin HEAD:refs/heads/patching/99.0.2 "$FIXTURE" snapshot` | `—` | — |
| 37 | existing-branch | `./oblt-actions/edot-release/start-patch` | `—` | `line`, `ref-name`, `dry-run`, `repository` |
| 38 | Step 38 | `exit 1` | `steps.existing-branch.outcome != 'failure'` | — |
| 39 | Step 39 | `"$FIXTURE" check-unchanged if "$START_PATCH" 2> "$RUNNER_TEMP/error.log"; then exit 1; fi cat "$RUNNER_TEMP/error.log" grep -Fx 'patching/99.0.2 already exists; cherry-pick further fixes by hand through pull requests in…` | `—` | `LINE` |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read, pull-requests: read`; job overrides: `none`. |
| Local actions | [`edot-release/start-patch/action.yml`](../../../edot-release/start-patch/action.yml); [usage README](../../../edot-release/start-patch/README.md) (called as `./oblt-actions/edot-release/start-patch`); checked out under `path: oblt-actions` — Cut the EDOT patch branch patching/X.Y.Z from the highest release tag of a line and cherry-pick merged main pull requests onto it. The caller checks out full history and tags and configures the Git identity and credentials. Inputs: `line`, `pull-requests`, `ref-name`, `dry-run`, `repository`, `github-token`. Declared outputs: none declared. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `is-success`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | No `secrets.*` references found in the workflow source. |

## Local scripts and sources

- [`edot-release/start-patch/start-patch.sh`](../../../edot-release/start-patch/start-patch.sh)
- [`edot-release/prepare-start/test-data/fixture.sh`](../../../edot-release/prepare-start/test-data/fixture.sh)

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-edot-release-start-patch.yml`](../test-edot-release-start-patch.yml#L1-420)
- Local action: [`edot-release/start-patch/action.yml`](../../../edot-release/start-patch/action.yml) and [`edot-release/start-patch/README.md`](../../../edot-release/start-patch/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
