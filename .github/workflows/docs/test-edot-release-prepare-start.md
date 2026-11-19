# test-edot-release-prepare-start

Test workflow for `edot-release-prepare-start`. Check an EDOT release dispatch, derive the release, and write the version file, applies_to entries, and release-notes section into the working tree. The caller must check out full history and tags.

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-edot-release-prepare-start.yml`](../test-edot-release-prepare-start.yml#L1-L503) |
| Trigger | `merge_group`; `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-edot-release-prepare-start.yml, edot-release/prepare-start/**, edot-release/version/**, edot-release/pr-range/**, edot-release/render-release-notes/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-edot-release-prepare-start.yml, edot-release/prepare-start/**, edot-release/version/**, edot-release/pr-range/**, edot-release/render-release-notes/**`) |

## Purpose

Test workflow for `edot-release-prepare-start`. Check an EDOT release dispatch, derive the release, and write the version file, applies_to entries, and release-notes section into the working tree. The caller must check out full history and tags.

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-edot-release-prepare-start.yml, edot-release/prepare-start/**, edot-release/version/**, edot-release/pr-range/**, edot-release/render-release-notes/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-edot-release-prepare-start.yml, edot-release/prepare-start/**, edot-release/version/**, edot-release/pr-range/**, edot-release/render-release-notes/**`). Conditions below can further restrict individual jobs or steps.

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
| 2 | Read release-note fixtures | `data=oblt-actions/edot-release/render-release-notes/test-data { echo "android=$(jq -c . "$data/android-1.10.0.json")" echo "ios=$(jq -c . "$data/ios-sample.json")" } >> "$GITHUB_OUTPUT"` | `—` | — |
| 3 | Create Android fixture | `"$FIXTURE" create android 1.10.0-SNAPSHOT v1.9.0 4da20136c2519785c63247bb20e7d383fab20528` | `—` | — |
| 4 | android | `./oblt-actions/edot-release/prepare-start` | `—` | `notes`, `ref`, `ref-name`, `repository` |
| 5 | Verify Android release changes | `"$FIXTURE" compare gradle.properties "$TEST_DATA/android/expected-gradle.properties" "$FIXTURE" compare docs/release-notes/index.md "$TEST_DATA/android/expected-index.md" "$FIXTURE" compare docs/reference/applies-to.md …` | `—` | `PREPARED`, `VERSION`, `PREVIOUS_TAG`, `RELEASE` |
| 6 | Create iOS fixture | `"$FIXTURE" create ios 2.2.0-SNAPSHOT 2.1.0 ff10c291ca210ccdf26ab86ad44ff5b910fa0d21` | `—` | — |
| 7 | ios | `./oblt-actions/edot-release/prepare-start` | `—` | `notes`, `ref`, `ref-name`, `repository` |
| 8 | Verify iOS release changes | `"$FIXTURE" compare Sources/apm-agent-ios/Version.swift "$TEST_DATA/ios/expected-Version.swift" "$FIXTURE" compare docs/release-notes/index.md "$TEST_DATA/ios/expected-index.md" "$FIXTURE" compare docs/reference/applies-…` | `—` | `PREPARED`, `VERSION`, `PREVIOUS_TAG`, `RELEASE` |
| 9 | Create Android patch fixture | `"$FIXTURE" create android 1.10.0 v1.10.0 4da20136c2519785c63247bb20e7d383fab20528` | `—` | — |
| 10 | patch | `./oblt-actions/edot-release/prepare-start` | `—` | `notes`, `ref`, `ref-name`, `repository` |
| 11 | Verify Android patch release changes | `grep -Fx 'version=1.10.1' gradle.properties "$FIXTURE" compare docs/reference/applies-to.md "$TEST_DATA/android/applies-to.md" test "$(grep -Fx -A1 '% next_release_notes' docs/release-notes/index.md \| tail -n 1)" \ = '#…` | `—` | `PREPARED`, `VERSION`, `PREVIOUS_TAG`, `RELEASE` |
| 12 | Create no-op fixture | `"$FIXTURE" create android 1.10.0-SNAPSHOT v1.9.0` | `—` | — |
| 13 | no-op | `./oblt-actions/edot-release/prepare-start` | `—` | `notes`, `ref`, `ref-name`, `repository` |
| 14 | Verify no-op | `"$FIXTURE" check-unchanged test "$PREPARED" = false test -z "$VERSION" test "$PREVIOUS_TAG" = v1.9.0 test -z "$RELEASE"` | `—` | `PREPARED`, `VERSION`, `PREVIOUS_TAG`, `RELEASE` |

### `invalid` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | `path` |
| 2 | Read release-note fixtures | `data=oblt-actions/edot-release/render-release-notes/test-data { echo "minor=$(jq -c . "$data/android-1.10.0.json")" echo "major=$(jq -c . "$data/ios-sample.json")" echo "uncategorized=$(jq -c '.uncategorized = [{"messag…` | `—` | — |
| 3 | Create fixture for a ref outside main and patching | `"$FIXTURE" create android 98.1.0-SNAPSHOT v98.0.0 4967b69e2f83588d572e721c4f34928b51ab003e` | `—` | — |
| 4 | feature-ref | `./oblt-actions/edot-release/prepare-start` | `—` | `notes`, `ref`, `ref-name`, `repository` |
| 5 | Step 5 | `exit 1` | `steps.feature-ref.outcome != 'failure'` | — |
| 6 | Step 6 | `"$FIXTURE" check-unchanged` | `—` | — |
| 7 | Create fixture with a release in flight | `"$FIXTURE" create android 98.1.0-SNAPSHOT v98.0.0 4967b69e2f83588d572e721c4f34928b51ab003e git push --quiet origin HEAD:refs/heads/releasing/99.0.0 "$FIXTURE" snapshot` | `—` | — |
| 8 | in-flight | `./oblt-actions/edot-release/prepare-start` | `—` | `notes`, `ref`, `ref-name`, `repository` |
| 9 | Step 9 | `exit 1` | `steps.in-flight.outcome != 'failure'` | — |
| 10 | Step 10 | `"$FIXTURE" check-unchanged` | `—` | — |
| 11 | Create fixture with an unexpected development version | `"$FIXTURE" create android 98.2.0-SNAPSHOT v98.0.0 4967b69e2f83588d572e721c4f34928b51ab003e` | `—` | — |
| 12 | development-version | `./oblt-actions/edot-release/prepare-start` | `—` | `notes`, `ref`, `ref-name`, `repository` |
| 13 | Step 13 | `exit 1` | `steps.development-version.outcome != 'failure'` | — |
| 14 | Step 14 | `"$FIXTURE" check-unchanged` | `—` | — |
| 15 | Create fixture for notes with uncategorized items | `"$FIXTURE" create android 98.1.0-SNAPSHOT v98.0.0 4967b69e2f83588d572e721c4f34928b51ab003e` | `—` | — |
| 16 | uncategorized | `./oblt-actions/edot-release/prepare-start` | `—` | `notes`, `ref`, `ref-name`, `repository` |
| 17 | Step 17 | `exit 1` | `steps.uncategorized.outcome != 'failure'` | — |
| 18 | Step 18 | `"$FIXTURE" check-unchanged` | `—` | — |
| 19 | Create fixture for a message with a Breaking prefix | `"$FIXTURE" create android 98.1.0-SNAPSHOT v98.0.0 4967b69e2f83588d572e721c4f34928b51ab003e` | `—` | — |
| 20 | prefixed-breaking | `./oblt-actions/edot-release/prepare-start` | `—` | `notes`, `ref`, `ref-name`, `repository` |
| 21 | Step 21 | `exit 1` | `steps.prefixed-breaking.outcome != 'failure'` | — |
| 22 | Step 22 | `"$FIXTURE" check-unchanged` | `—` | — |
| 23 | Create fixture for notes that are not JSON | `"$FIXTURE" create android 98.1.0-SNAPSHOT v98.0.0 4967b69e2f83588d572e721c4f34928b51ab003e` | `—` | — |
| 24 | invalid-json | `./oblt-actions/edot-release/prepare-start` | `—` | `notes`, `ref`, `ref-name`, `repository` |
| 25 | Step 25 | `exit 1` | `steps.invalid-json.outcome != 'failure'` | — |
| 26 | Step 26 | `"$FIXTURE" check-unchanged` | `—` | — |
| 27 | Create fixture whose index already has the release | `"$FIXTURE" create android 98.1.0-SNAPSHOT v98.0.0 "$FIXTURE" add-section 99.0.0 "$FIXTURE" commit 'Fixture change' 4967b69e2f83588d572e721c4f34928b51ab003e git push --quiet origin HEAD:refs/heads/main "$FIXTURE" snapshot` | `—` | — |
| 28 | existing-heading | `./oblt-actions/edot-release/prepare-start` | `—` | `notes`, `ref`, `ref-name`, `repository` |
| 29 | Step 29 | `exit 1` | `steps.existing-heading.outcome != 'failure'` | — |
| 30 | Step 30 | `"$FIXTURE" check-unchanged` | `—` | — |
| 31 | Create fixture for a patch that is already released | `"$FIXTURE" create android 99.0.0 v99.0.0 4967b69e2f83588d572e721c4f34928b51ab003e git tag v99.0.1 git push --quiet origin refs/tags/v99.0.1:refs/tags/v99.0.1 "$FIXTURE" snapshot` | `—` | — |
| 32 | released-patch | `./oblt-actions/edot-release/prepare-start` | `—` | `notes`, `ref`, `ref-name`, `repository` |
| 33 | Step 33 | `exit 1` | `steps.released-patch.outcome != 'failure'` | — |
| 34 | Step 34 | `"$FIXTURE" check-unchanged` | `—` | — |
| 35 | Create fixture for a breaking item on a patch branch | `"$FIXTURE" create android 99.0.0 v99.0.0 4967b69e2f83588d572e721c4f34928b51ab003e` | `—` | — |
| 36 | breaking-patch | `./oblt-actions/edot-release/prepare-start` | `—` | `notes`, `ref`, `ref-name`, `repository` |
| 37 | Step 37 | `exit 1` | `steps.breaking-patch.outcome != 'failure'` | — |
| 38 | Step 38 | `"$FIXTURE" check-unchanged` | `—` | — |
| 39 | Create fixture with two version lines | `"$FIXTURE" create android 98.1.0-SNAPSHOT v98.0.0 "$FIXTURE" duplicate-version-line "$FIXTURE" commit 'Fixture change' 4967b69e2f83588d572e721c4f34928b51ab003e git push --quiet origin HEAD:refs/heads/main "$FIXTURE" sna…` | `—` | — |
| 40 | two-version-lines | `./oblt-actions/edot-release/prepare-start` | `—` | `notes`, `ref`, `ref-name`, `repository` |
| 41 | Step 41 | `exit 1` | `steps.two-version-lines.outcome != 'failure'` | — |
| 42 | Step 42 | `"$FIXTURE" check-unchanged` | `—` | — |
| 43 | Create fixture with a missing configuration file | `"$FIXTURE" create android 98.1.0-SNAPSHOT v98.0.0 4967b69e2f83588d572e721c4f34928b51ab003e rm .github/edot-release.json "$FIXTURE" snapshot` | `—` | — |
| 44 | missing-config | `./oblt-actions/edot-release/prepare-start` | `—` | `notes`, `ref`, `ref-name`, `repository` |
| 45 | Step 45 | `exit 1` | `steps.missing-config.outcome != 'failure'` | — |
| 46 | Step 46 | `"$FIXTURE" check-unchanged` | `—` | — |
| 47 | Create fixture with a configuration file that is not JSON | `"$FIXTURE" create android 98.1.0-SNAPSHOT v98.0.0 4967b69e2f83588d572e721c4f34928b51ab003e echo '{"tagPrefix":' > .github/edot-release.json "$FIXTURE" snapshot` | `—` | — |
| 48 | config-not-json | `./oblt-actions/edot-release/prepare-start` | `—` | `notes`, `ref`, `ref-name`, `repository` |
| 49 | Step 49 | `exit 1` | `steps.config-not-json.outcome != 'failure'` | — |
| 50 | Step 50 | `"$FIXTURE" check-unchanged` | `—` | — |
| 51 | Create fixture with a configuration without docsUrl | `"$FIXTURE" create android 98.1.0-SNAPSHOT v98.0.0 4967b69e2f83588d572e721c4f34928b51ab003e "$FIXTURE" config 'del(.docsUrl)' "$FIXTURE" snapshot` | `—` | — |
| 52 | config-missing-key | `./oblt-actions/edot-release/prepare-start` | `—` | `notes`, `ref`, `ref-name`, `repository` |
| 53 | Step 53 | `exit 1` | `steps.config-missing-key.outcome != 'failure'` | — |
| 54 | Step 54 | `"$FIXTURE" check-unchanged` | `—` | — |
| 55 | Create fixture with a configuration with an unknown key | `"$FIXTURE" create android 98.1.0-SNAPSHOT v98.0.0 4967b69e2f83588d572e721c4f34928b51ab003e "$FIXTURE" config '. + {"tagPattern": "v*"}' "$FIXTURE" snapshot` | `—` | — |
| 56 | config-unknown-key | `./oblt-actions/edot-release/prepare-start` | `—` | `notes`, `ref`, `ref-name`, `repository` |
| 57 | Step 57 | `exit 1` | `steps.config-unknown-key.outcome != 'failure'` | — |
| 58 | Step 58 | `"$FIXTURE" check-unchanged` | `—` | — |
| 59 | Create fixture with a configuration whose tagPrefix is a number | `"$FIXTURE" create android 98.1.0-SNAPSHOT v98.0.0 4967b69e2f83588d572e721c4f34928b51ab003e "$FIXTURE" config '.tagPrefix = 1' "$FIXTURE" snapshot` | `—` | — |
| 60 | config-wrong-type | `./oblt-actions/edot-release/prepare-start` | `—` | `notes`, `ref`, `ref-name`, `repository` |
| 61 | Step 61 | `exit 1` | `steps.config-wrong-type.outcome != 'failure'` | — |
| 62 | Step 62 | `"$FIXTURE" check-unchanged` | `—` | — |
| 63 | Create fixture with a versionLine without a placeholder | `"$FIXTURE" create android 98.1.0-SNAPSHOT v98.0.0 4967b69e2f83588d572e721c4f34928b51ab003e "$FIXTURE" config '.versionLine = "version="' "$FIXTURE" snapshot` | `—` | — |
| 64 | config-version-line | `./oblt-actions/edot-release/prepare-start` | `—` | `notes`, `ref`, `ref-name`, `repository` |
| 65 | Step 65 | `exit 1` | `steps.config-version-line.outcome != 'failure'` | — |
| 66 | Step 66 | `"$FIXTURE" check-unchanged` | `—` | — |
| 67 | Create fixture with an empty stagePaths | `"$FIXTURE" create android 98.1.0-SNAPSHOT v98.0.0 4967b69e2f83588d572e721c4f34928b51ab003e "$FIXTURE" config '.stagePaths = []' "$FIXTURE" snapshot` | `—` | — |
| 68 | config-empty-stage-paths | `./oblt-actions/edot-release/prepare-start` | `—` | `notes`, `ref`, `ref-name`, `repository` |
| 69 | Step 69 | `exit 1` | `steps.config-empty-stage-paths.outcome != 'failure'` | — |
| 70 | Step 70 | `"$FIXTURE" check-unchanged` | `—` | — |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read, pull-requests: read`; job overrides: `none`. |
| Local actions | [`edot-release/prepare-start/action.yml`](../../../edot-release/prepare-start/action.yml); [usage README](../../../edot-release/prepare-start/README.md) (called as `./oblt-actions/edot-release/prepare-start`); checked out under `path: oblt-actions` — Check an EDOT release dispatch, derive the release, and write the version file, applies_to entries, and release-notes section into the working tree. The caller must check out full history and tags. Inputs: `notes`, `ref`, `ref-name`, `repository`, `github-token`. Declared outputs: `prepared`, `version`, `previous-tag`, `release`. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `android, ios, is-success, major, minor, prefixed-breaking, prepared, previous-tag, release, uncategorized, version`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | No `secrets.*` references found in the workflow source. |

## Local scripts and sources

- [`edot-release/prepare-start/prepare-start.sh`](../../../edot-release/prepare-start/prepare-start.sh)
- [`edot-release/prepare-start/test-data/fixture.sh`](../../../edot-release/prepare-start/test-data/fixture.sh)

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-edot-release-prepare-start.yml`](../test-edot-release-prepare-start.yml#L1-503)
- Local action: [`edot-release/prepare-start/action.yml`](../../../edot-release/prepare-start/action.yml) and [`edot-release/prepare-start/README.md`](../../../edot-release/prepare-start/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
