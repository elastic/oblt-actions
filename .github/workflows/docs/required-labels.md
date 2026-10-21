# required-labels

Validates pull-request labels against the release-drafter label categories.

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`required-labels.yml`](../required-labels.yml#L1-L36) |
| Trigger | `merge_group`; `workflow_dispatch`; `pull_request` (types: `opened, labeled, unlabeled, synchronize`) |

## Purpose

Validates pull-request labels against the release-drafter label categories.

The contribution guide documents the required-label check and its relationship to release labels.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `pull_request` (types: `opened, labeled, unlabeled, synchronize`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `check-labels` | `ubuntu-slim` | None declared | `Default GitHub condition` | `—` |

### `check-labels` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | get-labels | `labels=$(yq '[.categories[].labels] + .exclude-labels \| flatten \| unique \| sort \| @tsv' .github/release-drafter.yml \| tr '\t' ',') echo "labels=$labels" >> "${GITHUB_OUTPUT}"` | `—` | — |
| 3 | check-labels | `mheap/github-action-required-labels@23e10fde7e062233401931a0eece796cd9bf3177` | `—` | `mode`, `count`, `use_regex`, `add_comment`, `labels` |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read`; job overrides: `check-labels: contents: read, pull-requests: read`. |
| Local actions | None. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `labels`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | No `secrets.*` references found in the workflow source. |

## Operational notes

Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`required-labels.yml`](../required-labels.yml#L1-36)

- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
