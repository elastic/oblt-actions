# test-oblt-cli-cluster-create-custom

Test workflow for `oblt-cli-cluster-create-custom`. Run the oblt-cli wrapper to create a custom cluster.

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-oblt-cli-cluster-create-custom.yml`](../test-oblt-cli-cluster-create-custom.yml#L1-L127) |
| Trigger | `merge_group`; `workflow_dispatch` (inputs: `{'dry-run': {'description': 'Dry run', 'required': 'true', 'default': 'false', 'type': 'boolean'}}`); `pull_request` (branches: `main`; paths: `.github/workflows/test-oblt-cli-cluster-create-custom.yml, oblt-cli/cluster-create-custom/**`) |

## Purpose

Test workflow for `oblt-cli-cluster-create-custom`. Run the oblt-cli wrapper to create a custom cluster.

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch` (inputs: `{'dry-run': {'description': 'Dry run', 'required': 'true', 'default': 'false', 'type': 'boolean'}}`); `pull_request` (branches: `main`; paths: `.github/workflows/test-oblt-cli-cluster-create-custom.yml, oblt-cli/cluster-create-custom/**`). Conditions below can further restrict individual jobs or steps.

### Manual-dispatch inputs

| Input | Required | Default | Description |
| --- | --- | --- | --- |
| `dry-run` | true | false | Dry run |

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-slim` | no-gitops, gitops, multiline | `always()` | `—` |
| `no-gitops` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `gitops` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `multiline` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | check | `elastic/oblt-actions/check-dependent-jobs@v1` | `—` | `jobs` |
| 2 | Step 2 | `${{ steps.check.outputs.is-success }}` | `—` | — |

### `no-gitops` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `elastic/oblt-actions/git/setup@v1` | `—` | — |
| 3 | Get token | `actions/create-github-app-token@v3` | `—` | `app-id`, `private-key`, `permission-contents`, `repositories` |
| 4 | Compute expiry date | `echo "date=$(date -u -d '+1 hour' '+%Y-%m-%dT%H:%M:%SZ')" >> "$GITHUB_OUTPUT"` | `—` | — |
| 5 | Step 5 | `./oblt-cli/cluster-create-custom` | `—` | `github-token`, `template`, `cluster-name-prefix`, `gitops`, `dry-run`, `parameters`, `expiry-date`, `expire-in-hours` |

### `gitops` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `elastic/oblt-actions/git/setup@v1` | `—` | — |
| 3 | Get token | `actions/create-github-app-token@v3` | `—` | `app-id`, `private-key`, `permission-contents`, `repositories` |
| 4 | Compute expiry date | `echo "date=$(date -u -d '+1 hour' '+%Y-%m-%dT%H:%M:%SZ')" >> "$GITHUB_OUTPUT"` | `—` | — |
| 5 | Step 5 | `./oblt-cli/cluster-create-custom` | `—` | `github-token`, `template`, `cluster-name-prefix`, `gitops`, `dry-run`, `parameters`, `expiry-date`, `expire-in-hours` |

### `multiline` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `elastic/oblt-actions/git/setup@v1` | `—` | — |
| 3 | Get token | `actions/create-github-app-token@v3` | `—` | `app-id`, `private-key`, `permission-contents`, `repositories` |
| 4 | Compute expiry date | `echo "date=$(date -u -d '+1 hour' '+%Y-%m-%dT%H:%M:%SZ')" >> "$GITHUB_OUTPUT"` | `—` | — |
| 5 | Step 5 | `./oblt-cli/cluster-create-custom` | `—` | `github-token`, `template`, `cluster-name-prefix`, `gitops`, `dry-run`, `parameters`, `expiry-date`, `expire-in-hours` |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | `dry-run` |
| Permissions | Workflow: `contents: read`; job overrides: `none`. |
| Local actions | [`oblt-cli/cluster-create-custom/action.yml`](../../../oblt-cli/cluster-create-custom/action.yml); [usage README](../../../oblt-cli/cluster-create-custom/README.md) — Run the oblt-cli wrapper to create a custom cluster. Inputs: `template`, `parameters`, `github-token`, `cluster-name-prefix`, `cluster-name-suffix`, `slack-channel`, `username`, `gitops`, `dry-run`, `skip-random-name`, `wait`, `expiry-date`, `expire-in-hours`. Declared outputs: `cluster-name`. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `date, is-success, token`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | `OBS_AUTOMATION_APP_ID`, `OBS_AUTOMATION_APP_PEM` |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-oblt-cli-cluster-create-custom.yml`](../test-oblt-cli-cluster-create-custom.yml#L1-127)
- Local action: [`oblt-cli/cluster-create-custom/action.yml`](../../../oblt-cli/cluster-create-custom/action.yml) and [`oblt-cli/cluster-create-custom/README.md`](../../../oblt-cli/cluster-create-custom/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
