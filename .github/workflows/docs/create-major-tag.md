# create-major-tag

Force-pushes the matching major-version tag after a release is published.

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`create-major-tag.yml`](../create-major-tag.yml#L1-L23) |
| Trigger | `release` (types: `published`) |

## Purpose

Force-pushes the matching major-version tag after a release is published.

The release process documents that publishing a release triggers the `vX` major tag update.
See [RELEASE.md](../../../docs/RELEASE.md) for the repository guidance.

## When it runs

The workflow-level trigger is `release` (types: `published`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `create-major-tag` | `ubuntu-slim` | None declared | `Default GitHub condition` | `—` |

### `create-major-tag` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Get major version | `MAJOR_VERSION=$(echo "${GITHUB_REF#refs/tags/v}" \| awk -F. '{print $1}') echo "MAJOR_VERSION=${MAJOR_VERSION}" >> "${GITHUB_ENV}"` | `—` | — |
| 3 | Create major tag | `git tag "v${MAJOR_VERSION}" git push -f origin "refs/tags/v${MAJOR_VERSION}"` | `—` | — |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: write`; job overrides: `none`. |
| Local actions | None. |
| Outputs | No workflow/job outputs are declared. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | No `secrets.*` references found in the workflow source. |

## Operational notes

Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`create-major-tag.yml`](../create-major-tag.yml#L1-23)

- Rationale: [`RELEASE.md`](../../../docs/RELEASE.md)
- Release process: [`docs/RELEASE.md`](../../../docs/RELEASE.md).
