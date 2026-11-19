# test-edot-release-render-release-notes

Test workflow for `edot-release-render-release-notes`. Validate release-note JSON and render the EDOT Markdown release section.

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-edot-release-render-release-notes.yml`](../test-edot-release-render-release-notes.yml#L1-L193) |
| Trigger | `merge_group`; `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-edot-release-render-release-notes.yml, edot-release/render-release-notes/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-edot-release-render-release-notes.yml, edot-release/render-release-notes/**`) |

## Purpose

Test workflow for `edot-release-render-release-notes`. Validate release-note JSON and render the EDOT Markdown release section.

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-edot-release-render-release-notes.yml, edot-release/render-release-notes/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-edot-release-render-release-notes.yml, edot-release/render-release-notes/**`). Conditions below can further restrict individual jobs or steps.

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
| 2 | Step 2 | `./edot-release/render-release-notes` | `—` | `notes-file`, `version`, `output-file`, `repository`, `heading-anchor-base`, `subsection-anchor-base`, `release-date` |
| 3 | Verify Android section | `sed 's/[[:space:]]*$//' "$RUNNER_TEMP/android.md" > "$RUNNER_TEMP/android-clean.md" sed 's/[[:space:]]*$//' \ edot-release/render-release-notes/test-data/android-1.10.0.md \ > "$RUNNER_TEMP/android-want.md" diff "$RUNNE…` | `—` | — |
| 4 | Create literal path fixture | `cp edot-release/render-release-notes/test-data/ios-sample.json \ "$RUNNER_TEMP/notes\$literal.json"` | `—` | — |
| 5 | Step 5 | `./edot-release/render-release-notes` | `—` | `notes-file`, `version`, `output-file`, `repository`, `heading-anchor-base`, `subsection-anchor-base`, `release-date` |
| 6 | Verify iOS section | `diff "$RUNNER_TEMP/ios\$literal.md" edot-release/render-release-notes/test-data/ios-sample.md` | `—` | — |

### `invalid` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Create rejection fixtures | `jq '.uncategorized = [{"message":"Classify me"}]' \ edot-release/render-release-notes/test-data/ios-sample.json \ > "$RUNNER_TEMP/uncategorized.json" jq '.featuresEnhancements[0].message = "[Breaking] Duplicate signal"'…` | `—` | — |
| 3 | uncategorized | `./edot-release/render-release-notes` | `—` | `notes-file`, `version`, `output-file`, `repository`, `heading-anchor-base`, `subsection-anchor-base` |
| 4 | Step 4 | `exit 1` | `steps.uncategorized.outcome != 'failure'` | — |
| 5 | prefixed-breaking | `./edot-release/render-release-notes` | `—` | `notes-file`, `version`, `output-file`, `repository`, `heading-anchor-base`, `subsection-anchor-base` |
| 6 | Step 6 | `exit 1` | `steps.prefixed-breaking.outcome != 'failure'` | — |
| 7 | empty | `./edot-release/render-release-notes` | `—` | `notes-file`, `version`, `output-file`, `repository`, `heading-anchor-base`, `subsection-anchor-base` |
| 8 | Step 8 | `exit 1` | `steps.empty.outcome != 'failure'` | — |
| 9 | invalid-version | `./edot-release/render-release-notes` | `—` | `notes-file`, `version`, `output-file`, `repository`, `heading-anchor-base`, `subsection-anchor-base` |
| 10 | Step 10 | `exit 1` | `steps.invalid-version.outcome != 'failure'` | — |
| 11 | invalid-json | `./edot-release/render-release-notes` | `—` | `notes-file`, `version`, `output-file`, `repository`, `heading-anchor-base`, `subsection-anchor-base` |
| 12 | Step 12 | `exit 1` | `steps.invalid-json.outcome != 'failure'` | — |
| 13 | missing-heading-anchor | `./edot-release/render-release-notes` | `—` | `notes-file`, `version`, `output-file`, `repository`, `heading-anchor-base`, `subsection-anchor-base` |
| 14 | Step 14 | `exit 1` | `steps.missing-heading-anchor.outcome != 'failure'` | — |
| 15 | missing-subsection-anchor | `./edot-release/render-release-notes` | `—` | `notes-file`, `version`, `output-file`, `repository`, `heading-anchor-base`, `subsection-anchor-base` |
| 16 | Step 16 | `exit 1` | `steps.missing-subsection-anchor.outcome != 'failure'` | — |
| 17 | Reject an empty repository | `if RELEASE_REPOSITORY='' edot-release/render-release-notes/render-release-notes.sh \ edot-release/render-release-notes/test-data/ios-sample.json 2.2.0 \ elastic-apm-220 elastic-apm-ios-agent-220 > /dev/null; then exit 1…` | `—` | — |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read`; job overrides: `none`. |
| Local actions | [`edot-release/render-release-notes/action.yml`](../../../edot-release/render-release-notes/action.yml); [usage README](../../../edot-release/render-release-notes/README.md) — Validate release-note JSON and render the EDOT Markdown release section. Inputs: `notes-file`, `version`, `output-file`, `repository`, `heading-anchor-base`, `subsection-anchor-base`, `release-date`. Declared outputs: none declared. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `is-success`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | No `secrets.*` references found in the workflow source. |

## Local scripts and sources

- [`edot-release/render-release-notes/render-release-notes.sh`](../../../edot-release/render-release-notes/render-release-notes.sh)

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-edot-release-render-release-notes.yml`](../test-edot-release-render-release-notes.yml#L1-193)
- Local action: [`edot-release/render-release-notes/action.yml`](../../../edot-release/render-release-notes/action.yml) and [`edot-release/render-release-notes/README.md`](../../../edot-release/render-release-notes/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
