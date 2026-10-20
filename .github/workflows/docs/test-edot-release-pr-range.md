# test-edot-release-pr-range

Test workflow for `edot-release-pr-range`. List the pull requests contributing to an EDOT release range. The caller must check out full history and tags.

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-edot-release-pr-range.yml`](../test-edot-release-pr-range.yml#L1-L95) |
| Trigger | `merge_group`; `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-edot-release-pr-range.yml, edot-release/pr-range/**, edot-release/version/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-edot-release-pr-range.yml, edot-release/pr-range/**, edot-release/version/**`) |

## Purpose

Test workflow for `edot-release-pr-range`. List the pull requests contributing to an EDOT release range. The caller must check out full history and tags.

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-edot-release-pr-range.yml, edot-release/pr-range/**, edot-release/version/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-edot-release-pr-range.yml, edot-release/pr-range/**, edot-release/version/**`). Conditions below can further restrict individual jobs or steps.

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
| 1 | Step 1 | `actions/checkout@v7` | `—` | `fetch-depth` |
| 2 | range | `./edot-release/pr-range` | `—` | `ref`, `previous-tag`, `tag-prefix`, `repository` |
| 3 | Create literal ref fixture | `git branch "edot-release-literal-\$value" v1.41.3` | `—` | — |
| 4 | literal-ref | `./edot-release/pr-range` | `—` | `ref`, `previous-tag`, `tag-prefix`, `repository` |
| 5 | Verify ranges | `for range in "$RANGE" "$LITERAL_RANGE"; do jq -e ' .previousTag == "v1.41.2" and (.pullRequests \| map(.number) == [1135]) ' <<<"$range" done` | `—` | `RANGE`, `LITERAL_RANGE` |

### `invalid` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | `fetch-depth` |
| 2 | missing-tag | `./edot-release/pr-range` | `—` | `ref`, `previous-tag`, `tag-prefix`, `repository` |
| 3 | Step 3 | `exit 1` | `steps.missing-tag.outcome != 'failure'` | — |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read, pull-requests: read`; job overrides: `none`. |
| Local actions | [`edot-release/pr-range/action.yml`](../../../edot-release/pr-range/action.yml); [usage README](../../../edot-release/pr-range/README.md) — List the pull requests contributing to an EDOT release range. The caller must check out full history and tags. Inputs: `ref`, `previous-tag`, `tag-prefix`, `repository`, `github-token`. Declared outputs: `range`. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `is-success, range`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | No `secrets.*` references found in the workflow source. |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-edot-release-pr-range.yml`](../test-edot-release-pr-range.yml#L1-95)
- Local action: [`edot-release/pr-range/action.yml`](../../../edot-release/pr-range/action.yml) and [`edot-release/pr-range/README.md`](../../../edot-release/pr-range/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
