# test-oblt-cli-setup

Test workflow for `oblt-cli-setup`. Setup oblt-cli for use in GitHub Actions workflows.

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-oblt-cli-setup.yml`](../test-oblt-cli-setup.yml#L1-L228) |
| Trigger | `merge_group`; `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-oblt-cli-setup.yml, oblt-cli/setup/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-oblt-cli-setup.yml, oblt-cli/setup/**`) |

## Purpose

Test workflow for `oblt-cli-setup`. Setup oblt-cli for use in GitHub Actions workflows.

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-oblt-cli-setup.yml, oblt-cli/setup/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-oblt-cli-setup.yml, oblt-cli/setup/**`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-slim` | version, version-file, default-version, tools-versions, non-existing-file, both-version-and-version-file, default-username, explicit-username | `Default GitHub condition` | `—` |
| `version` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `version-file` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `default-version` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `tools-versions` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `non-existing-file` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `both-version-and-version-file` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `default-username` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |
| `explicit-username` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | check | `elastic/oblt-actions/check-dependent-jobs@v1` | `—` | `jobs` |
| 2 | Step 2 | `${{ steps.check.outputs.is-success }}` | `—` | — |

### `version` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Get token | `actions/create-github-app-token@v3` | `—` | `app-id`, `private-key`, `permission-contents`, `repositories` |
| 3 | Step 3 | `./oblt-cli/setup` | `—` | `version`, `github-token` |
| 4 | Verify oblt-cli version | `version=$(oblt-cli version 2>&1) [[ "$version" == *"version 7.2.2"* ]]` | `—` | — |

### `version-file` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Get token | `actions/create-github-app-token@v3` | `—` | `app-id`, `private-key`, `permission-contents`, `repositories` |
| 3 | Setup version file | `echo "7.2.5" > .oblt-cli-version` | `—` | — |
| 4 | Step 4 | `./oblt-cli/setup` | `—` | `github-token`, `version-file` |
| 5 | Verify oblt-cli version | `version=$(oblt-cli version 2>&1) [[ "$version" == *"version 7.2.5"* ]]` | `—` | — |

### `default-version` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Get token | `actions/create-github-app-token@v3` | `—` | `app-id`, `private-key`, `permission-contents`, `repositories` |
| 3 | Step 3 | `./oblt-cli/setup` | `—` | `github-token` |
| 4 | Verify oblt-cli version | `version=$(oblt-cli version 2>&1) default_version=$(cat ./oblt-cli/setup/.default-oblt-cli-version) [[ "$version" == *"version ${default_version}"* ]]` | `—` | — |

### `tools-versions` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Get token | `actions/create-github-app-token@v3` | `—` | `app-id`, `private-key`, `permission-contents`, `repositories` |
| 3 | Setup version file | `cat <<EOF > .tool-versions oblt-cli 7.2.5 # This is a comment that contains oblt-cli # This is another comment that contains oblt-cli ruby 2.5.3 nodejs 10.15.0 EOF` | `—` | — |
| 4 | Step 4 | `./oblt-cli/setup` | `—` | `github-token`, `version-file` |
| 5 | Verify oblt-cli version | `version=$(oblt-cli version 2>&1) [[ "$version" == *"version 7.2.5"* ]]` | `—` | — |

### `non-existing-file` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Get token | `actions/create-github-app-token@v3` | `—` | `app-id`, `private-key`, `permission-contents`, `repositories` |
| 3 | oblt-cli-setup | `./oblt-cli/setup` | `—` | `github-token`, `version-file` |
| 4 | Verify step failed | `exit 1` | `steps.oblt-cli-setup.outcome != 'failure'` | — |

### `both-version-and-version-file` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Get token | `actions/create-github-app-token@v3` | `—` | `app-id`, `private-key`, `permission-contents`, `repositories` |
| 3 | oblt-cli-setup | `./oblt-cli/setup` | `—` | `github-token`, `version`, `version-file` |
| 4 | Verify oblt-cli version | `version=$(oblt-cli version 2>&1) [[ "$version" == *"version 7.3.0"* ]]` | `—` | — |

### `default-username` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Get token | `actions/create-github-app-token@v3` | `—` | `app-id`, `private-key`, `permission-contents`, `repositories` |
| 3 | Step 3 | `./oblt-cli/setup` | `—` | `github-token` |
| 4 | Verify default username derived from repository name | `expected=$(echo "${GITHUB_REPOSITORY##*/}" \| tr '[:upper:]' '[:lower:]' \| tr -cd 'a-z0-9_-') echo "Expected username: ${expected}" grep -i "username" ~/.oblt-cli/config.yaml \| grep -i "${expected}"` | `—` | — |

### `explicit-username` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Get token | `actions/create-github-app-token@v3` | `—` | `app-id`, `private-key`, `permission-contents`, `repositories` |
| 3 | Step 3 | `./oblt-cli/setup` | `—` | `github-token`, `username` |
| 4 | Verify explicit username is sanitized and used | `grep -i "username" ~/.oblt-cli/config.yaml \| grep -i "myuser-123"` | `—` | — |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read`; job overrides: `none`. |
| Local actions | [`oblt-cli/setup/action.yml`](../../../oblt-cli/setup/action.yml); [usage README](../../../oblt-cli/setup/README.md) — Setup oblt-cli for use in GitHub Actions workflows. Inputs: `github-token`, `slack-channel`, `username`, `version`, `version-file`. Declared outputs: none declared. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `is-success, token`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | `OBS_AUTOMATION_APP_ID`, `OBS_AUTOMATION_APP_PEM` |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-oblt-cli-setup.yml`](../test-oblt-cli-setup.yml#L1-228)
- Local action: [`oblt-cli/setup/action.yml`](../../../oblt-cli/setup/action.yml) and [`oblt-cli/setup/README.md`](../../../oblt-cli/setup/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
