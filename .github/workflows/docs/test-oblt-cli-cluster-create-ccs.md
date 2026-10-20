# test-oblt-cli-cluster-create-ccs

Test workflow for `oblt-cli-cluster-create-ccs`. Run the oblt-cli wrapper to create a CCS cluster.

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-oblt-cli-cluster-create-ccs.yml`](../test-oblt-cli-cluster-create-ccs.yml#L1-L59) |
| Trigger | `merge_group`; `workflow_dispatch` (inputs: `{'dry-run': {'description': 'Dry run', 'required': 'true', 'default': 'false', 'type': 'boolean'}}`); `push` (branches: `main`; paths: `.github/workflows/test-oblt-cli-cluster-create-ccs.yml, oblt-cli/cluster-create-ccs/**`) |

## Purpose

Test workflow for `oblt-cli-cluster-create-ccs`. Run the oblt-cli wrapper to create a CCS cluster.

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch` (inputs: `{'dry-run': {'description': 'Dry run', 'required': 'true', 'default': 'false', 'type': 'boolean'}}`); `push` (branches: `main`; paths: `.github/workflows/test-oblt-cli-cluster-create-ccs.yml, oblt-cli/cluster-create-ccs/**`). Conditions below can further restrict individual jobs or steps.

### Manual-dispatch inputs

| Input | Required | Default | Description |
| --- | --- | --- | --- |
| `dry-run` | true | false | Dry run |

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-slim` | dry-run | `always()` | `—` |
| `dry-run` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | check | `elastic/oblt-actions/check-dependent-jobs@v1` | `—` | `jobs` |
| 2 | Step 2 | `${{ steps.check.outputs.is-success }}` | `—` | — |

### `dry-run` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `elastic/oblt-actions/git/setup@v1` | `—` | — |
| 3 | Get token | `actions/create-github-app-token@v3` | `—` | `app-id`, `private-key`, `permission-contents`, `permission-pull-requests`, `repositories` |
| 4 | create | `./oblt-cli/cluster-create-ccs` | `—` | `github-token`, `remote-cluster`, `cluster-name-prefix`, `gitops`, `dry-run` |
| 5 | Assert is not empty | `test -n "${{steps.create.outputs.cluster-name}}"` | `—` | — |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | `dry-run` |
| Permissions | Workflow: `contents: read`; job overrides: `none`. |
| Local actions | [`oblt-cli/cluster-create-ccs/action.yml`](../../../oblt-cli/cluster-create-ccs/action.yml); [usage README](../../../oblt-cli/cluster-create-ccs/README.md) — Run the oblt-cli wrapper to create a CCS cluster. Inputs: `remote-cluster`, `github-token`, `cluster-name-prefix`, `cluster-name-suffix`, `elasticsearch-docker-image`, `slack-channel`, `username`, `gitops`, `dry-run`, `wait`, `expiry-date`. Declared outputs: `cluster-name`. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `cluster-name, is-success, token`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | `OBS_AUTOMATION_APP_ID`, `OBS_AUTOMATION_APP_PEM` |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-oblt-cli-cluster-create-ccs.yml`](../test-oblt-cli-cluster-create-ccs.yml#L1-59)
- Local action: [`oblt-cli/cluster-create-ccs/action.yml`](../../../oblt-cli/cluster-create-ccs/action.yml) and [`oblt-cli/cluster-create-ccs/README.md`](../../../oblt-cli/cluster-create-ccs/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
