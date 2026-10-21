# test-edot-release-publish-guard

Test workflow for `edot-release-publish-guard`. Check that a merged EDOT preparation pull request may publish its release, and report whether its tag already exists.

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-edot-release-publish-guard.yml`](../test-edot-release-publish-guard.yml#L1-L257) |
| Trigger | `merge_group`; `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-edot-release-publish-guard.yml, edot-release/publish-guard/**, edot-release/prepare-start/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-edot-release-publish-guard.yml, edot-release/publish-guard/**, edot-release/prepare-start/**`) |

## Purpose

Test workflow for `edot-release-publish-guard`. Check that a merged EDOT preparation pull request may publish its release, and report whether its tag already exists.

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-edot-release-publish-guard.yml, edot-release/publish-guard/**, edot-release/prepare-start/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-edot-release-publish-guard.yml, edot-release/publish-guard/**, edot-release/prepare-start/**`). Conditions below can further restrict individual jobs or steps.

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
| 2 | Create merged preparation commit | `"$FIXTURE" create android 98.1.0-SNAPSHOT v98.0.0 "$FIXTURE" set-version 99.0.0 "$FIXTURE" add-section 99.0.0 sha=$("$FIXTURE" commit 'Prepare release 99.0.0') git push --quiet origin "$sha:refs/heads/releasing/99.0.0" …` | `—` | — |
| 3 | untagged | `./oblt-actions/edot-release/publish-guard` | `—` | `base-ref`, `head-ref`, `merge-commit` |
| 4 | Verify untagged release | `test "$VERSION" = 99.0.0 test "$TAG_EXISTS" = false jq -e --arg sha "$SHA" ' . == {sha: $sha, version: "99.0.0", baseRef: "releasing/99.0.0", tagExists: false} ' <<<"$RELEASE"` | `—` | `SHA`, `VERSION`, `TAG_EXISTS`, `RELEASE` |
| 5 | Tag the merge commit on origin | `git push --quiet origin "$SHA:refs/tags/v99.0.0"` | `—` | `SHA` |
| 6 | tagged | `./oblt-actions/edot-release/publish-guard` | `—` | `base-ref`, `head-ref`, `merge-commit` |
| 7 | Verify tagged release | `test "$VERSION" = 99.0.0 test "$TAG_EXISTS" = true jq -e --arg sha "$SHA" ' . == {sha: $sha, version: "99.0.0", baseRef: "releasing/99.0.0", tagExists: true} ' <<<"$RELEASE"` | `—` | `SHA`, `VERSION`, `TAG_EXISTS`, `RELEASE` |
| 8 | Commit the next development version on releasing/99.0.0 | `git switch --quiet -c releasing/99.0.0 "$SHA" "$FIXTURE" set-version 99.1.0-SNAPSHOT "$FIXTURE" commit 'Prepare for the next release' > /dev/null git push --quiet origin refs/heads/releasing/99.0.0:refs/heads/releasing/…` | `—` | `SHA` |
| 9 | bumped | `./oblt-actions/edot-release/publish-guard` | `—` | `base-ref`, `head-ref`, `merge-commit` |
| 10 | Verify release under the bump commit | `jq -e --arg sha "$SHA" ' . == {sha: $sha, version: "99.0.0", baseRef: "releasing/99.0.0", tagExists: true} ' <<<"$RELEASE"` | `—` | `SHA`, `RELEASE` |

### `invalid` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | `path` |
| 2 | Create fixture | `"$FIXTURE" create android 98.1.0-SNAPSHOT v98.0.0 "$FIXTURE" set-version 99.0.0 "$FIXTURE" add-section 99.0.0 release=$("$FIXTURE" commit 'Prepare release 99.0.0') "$FIXTURE" set-version 99.1.0-SNAPSHOT development=$("$…` | `—` | — |
| 3 | other-head | `./oblt-actions/edot-release/publish-guard` | `—` | `base-ref`, `head-ref`, `merge-commit` |
| 4 | Step 4 | `exit 1` | `steps.other-head.outcome != 'failure'` | — |
| 5 | Step 5 | `"$FIXTURE" check-unchanged` | `—` | — |
| 6 | other-base | `./oblt-actions/edot-release/publish-guard` | `—` | `base-ref`, `head-ref`, `merge-commit` |
| 7 | Step 7 | `exit 1` | `steps.other-base.outcome != 'failure'` | — |
| 8 | Step 8 | `"$FIXTURE" check-unchanged` | `—` | — |
| 9 | tag-elsewhere | `./oblt-actions/edot-release/publish-guard` | `—` | `base-ref`, `head-ref`, `merge-commit` |
| 10 | Step 10 | `exit 1` | `steps.tag-elsewhere.outcome != 'failure'` | — |
| 11 | Step 11 | `"$FIXTURE" check-unchanged` | `—` | — |
| 12 | Abbreviate the merge commit | `echo "sha=${RELEASE:0:12}" >> "$GITHUB_OUTPUT"` | `—` | `RELEASE` |
| 13 | short-sha | `./oblt-actions/edot-release/publish-guard` | `—` | `base-ref`, `head-ref`, `merge-commit` |
| 14 | Step 14 | `exit 1` | `steps.short-sha.outcome != 'failure'` | — |
| 15 | Step 15 | `"$FIXTURE" check-unchanged` | `—` | — |
| 16 | development-version | `./oblt-actions/edot-release/publish-guard` | `—` | `base-ref`, `head-ref`, `merge-commit` |
| 17 | Step 17 | `exit 1` | `steps.development-version.outcome != 'failure'` | — |
| 18 | Step 18 | `"$FIXTURE" check-unchanged` | `—` | — |
| 19 | Create fixture with a commit outside the releasing branch | `"$FIXTURE" create android 98.1.0-SNAPSHOT v98.0.0 git switch --quiet -c releasing/99.0.0 "$FIXTURE" set-version 99.0.0 "$FIXTURE" add-section 99.0.0 "$FIXTURE" commit 'Prepare release 99.0.0' > /dev/null git switch --qu…` | `—` | — |
| 20 | off-branch | `./oblt-actions/edot-release/publish-guard` | `—` | `base-ref`, `head-ref`, `merge-commit` |
| 21 | Step 21 | `exit 1` | `steps.off-branch.outcome != 'failure'` | — |
| 22 | Step 22 | `"$FIXTURE" check-unchanged` | `—` | — |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read, pull-requests: read`; job overrides: `none`. |
| Local actions | [`edot-release/publish-guard/action.yml`](../../../edot-release/publish-guard/action.yml); [usage README](../../../edot-release/publish-guard/README.md) (called as `./oblt-actions/edot-release/publish-guard`); checked out under `path: oblt-actions` — Check that a merged EDOT preparation pull request may publish its release, and report whether its tag already exists. Inputs: `base-ref`, `head-ref`, `merge-commit`. Declared outputs: `version`, `tag-exists`, `release`. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `development, is-success, release, sha, tag-exists, version`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | No `secrets.*` references found in the workflow source. |

## Local scripts and sources

- [`edot-release/publish-guard/publish-guard.sh`](../../../edot-release/publish-guard/publish-guard.sh)
- [`edot-release/prepare-start/test-data/fixture.sh`](../../../edot-release/prepare-start/test-data/fixture.sh)

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-edot-release-publish-guard.yml`](../test-edot-release-publish-guard.yml#L1-257)
- Local action: [`edot-release/publish-guard/action.yml`](../../../edot-release/publish-guard/action.yml) and [`edot-release/publish-guard/README.md`](../../../edot-release/publish-guard/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
