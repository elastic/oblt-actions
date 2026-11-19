# test-edot-release-draft-release-notes

Test workflow for `edot-release-draft-release-notes`. Draft EDOT release-note JSON from the pull requests in a release range.

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-edot-release-draft-release-notes.yml`](../test-edot-release-draft-release-notes.yml#L1-L164) |
| Trigger | `merge_group`; `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-edot-release-draft-release-notes.yml, edot-release/draft-release-notes/**, edot-release/pr-range/**, edot-release/version/**, edot-release/prepare-start/config.sh, edot-release/prepare-start/test-data/android/edot-release.json`); `pull_request` (branches: `main`; paths: `.github/workflows/test-edot-release-draft-release-notes.yml, edot-release/draft-release-notes/**, edot-release/pr-range/**, edot-release/version/**, edot-release/prepare-start/config.sh, edot-release/prepare-start/test-data/android/edot-release.json`) |

## Purpose

Test workflow for `edot-release-draft-release-notes`. Draft EDOT release-note JSON from the pull requests in a release range.

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-edot-release-draft-release-notes.yml, edot-release/draft-release-notes/**, edot-release/pr-range/**, edot-release/version/**, edot-release/prepare-start/config.sh, edot-release/prepare-start/test-data/android/edot-release.json`); `pull_request` (branches: `main`; paths: `.github/workflows/test-edot-release-draft-release-notes.yml, edot-release/draft-release-notes/**, edot-release/pr-range/**, edot-release/version/**, edot-release/prepare-start/config.sh, edot-release/prepare-start/test-data/android/edot-release.json`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-slim` | valid, grouping, invalid | `always()` | `—` |
| `valid` | `ubuntu-slim` | None declared | `Default GitHub condition` | `—` |
| `grouping` | `ubuntu-slim` | None declared | `Default GitHub condition` | `—` |
| `invalid` | `ubuntu-slim` | None declared | `Default GitHub condition` | `—` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | check | `elastic/oblt-actions/check-dependent-jobs@v1` | `—` | `jobs` |
| 2 | Step 2 | `${{ steps.check.outputs.is-success }}` | `—` | — |

### `valid` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | `fetch-depth` |
| 2 | notes | `./edot-release/draft-release-notes` | `—` | `ref`, `ref-name`, `previous-tag`, `tag-prefix`, `repository` |
| 3 | Create literal ref fixture | `git branch "edot-release-literal-\$value" v1.41.3` | `—` | — |
| 4 | literal-ref | `./edot-release/draft-release-notes` | `—` | `ref`, `ref-name`, `previous-tag`, `tag-prefix`, `repository` |
| 5 | Verify notes | `for notes in "$NOTES" "$LITERAL_NOTES"; do jq -e ' (.dependencies \| length) == 0 and (.featuresEnhancements \| length) == 0 and (.fixes \| length) == 0 and (.uncategorized \| map(.prId) == ["1135"]) ' <<<"$notes" done` | `—` | `NOTES`, `LITERAL_NOTES` |
| 6 | Create release configuration fixture | `jq '.tagPrefix = "edot-release-test-"' \ edot-release/prepare-start/test-data/android/edot-release.json \ > .github/edot-release.json git tag edot-release-test-1.41.2 v1.41.2` | `—` | — |
| 7 | config-prefix | `./edot-release/draft-release-notes` | `—` | `ref`, `ref-name`, `repository` |
| 8 | Verify notes drafted with the configured prefix | `jq -e ' (.dependencies \| length) == 0 and (.featuresEnhancements \| length) == 0 and (.fixes \| length) == 0 and (.uncategorized \| map(.prId) == ["1135"]) ' <<<"$NOTES"` | `—` | `NOTES` |

### `grouping` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `jq -f edot-release/draft-release-notes/group.jq \ edot-release/draft-release-notes/test-data/range.json \ > "$RUNNER_TEMP/notes.json" diff "$RUNNER_TEMP/notes.json" \ edot-release/draft-release-notes/test-data/notes.json` | `—` | — |

### `invalid` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | `fetch-depth` |
| 2 | missing-tag | `./edot-release/draft-release-notes` | `—` | `ref`, `ref-name`, `previous-tag`, `tag-prefix`, `repository` |
| 3 | Step 3 | `exit 1` | `steps.missing-tag.outcome != 'failure'` | — |
| 4 | Create malformed release configuration | `echo '{"tagPrefix": "v", "unknownKey": true}' > .github/edot-release.json` | `—` | — |
| 5 | malformed-config | `./edot-release/draft-release-notes` | `—` | `ref`, `ref-name`, `previous-tag`, `repository` |
| 6 | Step 6 | `exit 1` | `steps.malformed-config.outcome != 'failure'` | — |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read, pull-requests: read`; job overrides: `none`. |
| Local actions | [`edot-release/draft-release-notes/action.yml`](../../../edot-release/draft-release-notes/action.yml); [usage README](../../../edot-release/draft-release-notes/README.md) — Draft EDOT release-note JSON from the pull requests in a release range. Inputs: `ref`, `ref-name`, `previous-tag`, `tag-prefix`, `repository`, `github-token`. Declared outputs: `notes`. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `is-success, notes`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | No `secrets.*` references found in the workflow source. |

## Local scripts and sources

- [`edot-release/draft-release-notes/../prepare-start/config.sh`](../../../edot-release/prepare-start/config.sh)
- [`edot-release/draft-release-notes/draft-release-notes.sh`](../../../edot-release/draft-release-notes/draft-release-notes.sh)
- [`edot-release/prepare-start/config.sh`](../../../edot-release/prepare-start/config.sh)
- [`edot-release/draft-release-notes/group.jq`](../../../edot-release/draft-release-notes/group.jq)

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-edot-release-draft-release-notes.yml`](../test-edot-release-draft-release-notes.yml#L1-164)
- Local action: [`edot-release/draft-release-notes/action.yml`](../../../edot-release/draft-release-notes/action.yml) and [`edot-release/draft-release-notes/README.md`](../../../edot-release/draft-release-notes/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
