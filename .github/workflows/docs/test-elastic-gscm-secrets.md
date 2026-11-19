# test-elastic-gscm-secrets

Test workflow for `elastic-gscm-secrets`. Retrieve a Google Secret Manager dotenv secret, mask its values, and export them as environment variables.

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-elastic-gscm-secrets.yml`](../test-elastic-gscm-secrets.yml#L1-L38) |
| Trigger | `merge_group`; `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-elastic-gscm-secrets.yml, elastic/gscm-secrets/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-elastic-gscm-secrets.yml, elastic/gscm-secrets/**`) |

## Purpose

Test workflow for `elastic-gscm-secrets`. Retrieve a Google Secret Manager dotenv secret, mask its values, and export them as environment variables.

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-elastic-gscm-secrets.yml, elastic/gscm-secrets/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-elastic-gscm-secrets.yml, elastic/gscm-secrets/**`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `./elastic/gscm-secrets` | `—` | `oblt-cluster` |
| 3 | Assert credentials were exported | `test -n "${ELASTICSEARCH_HOST}" test -n "${ELASTICSEARCH_USERNAME}" test -n "${ELASTICSEARCH_PASSWORD}" test -n "${KIBANA_HOST}" test -n "${KIBANA_USERNAME}" test -n "${KIBANA_PASSWORD}"` | `—` | — |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read, id-token: write`; job overrides: `none`. |
| Local actions | [`elastic/gscm-secrets/action.yml`](../../../elastic/gscm-secrets/action.yml); [usage README](../../../elastic/gscm-secrets/README.md) — Retrieve a Google Secret Manager dotenv secret, mask its values, and export them as environment variables. Inputs: `oblt-cluster`. Declared outputs: none declared. |
| Outputs | No workflow/job outputs are declared. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | `yml` |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-elastic-gscm-secrets.yml`](../test-elastic-gscm-secrets.yml#L1-38)
- Local action: [`elastic/gscm-secrets/action.yml`](../../../elastic/gscm-secrets/action.yml) and [`elastic/gscm-secrets/README.md`](../../../elastic/gscm-secrets/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
