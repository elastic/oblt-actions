# test-kibana-docker-image

Test workflow for `kibana-docker-image`. An Action to build and push Kibana docker images given a git ref.

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-kibana-docker-image.yml`](../test-kibana-docker-image.yml#L1-L78) |
| Trigger | `merge_group`; `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-kibana-docker-image.yml, kibana-docker-image/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-kibana-docker-image.yml, kibana-docker-image/**`) |

## Purpose

Test workflow for `kibana-docker-image`. An Action to build and push Kibana docker images given a git ref.

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `push` (branches: `main`; paths: `.github/workflows/test-kibana-docker-image.yml, kibana-docker-image/**`); `pull_request` (branches: `main`; paths: `.github/workflows/test-kibana-docker-image.yml, kibana-docker-image/**`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-latest` | None declared | `Default GitHub condition` | `{'include': [{'serverless': 'false'}]}` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Free Disk Space (Ubuntu) | `jlumbroso/free-disk-space@ceedf095f4ec1a097402bc6bd80831f2e1a6fde6` | `${{ github.event_name != 'merge_group' }}` | `tool-cache`, `android`, `dotnet`, `haskell`, `large-packages`, `docker-images`, `swap-storage` |
| 3 | Log in to the Elastic Container registry | `docker/login-action@dbcb813823bdd20940b903addbd779551569679f` | `${{ github.event_name != 'merge_group' }}` | `registry`, `username`, `password` |
| 4 | kibana-docker-image | `./kibana-docker-image` | `${{ github.event_name != 'merge_group' }}` | `serverless` |
| 5 | validate | `echo "${STACK_VERSION:?}" echo "${GIT_COMMIT_SHA:?}" echo "${DOCKER_IMAGE_REF:?}" docker pull "${DOCKER_IMAGE_REF}"` | `${{ github.event_name != 'merge_group' }}` | `DOCKER_IMAGE_REF`, `GIT_COMMIT_SHA`, `STACK_VERSION` |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read`; job overrides: `none`. |
| Local actions | [`kibana-docker-image/action.yml`](../../../kibana-docker-image/action.yml); [usage README](../../../kibana-docker-image/README.md) — An Action to build and push Kibana docker images given a git ref. Inputs: `github-repository`, `git-ref`, `serverless`, `docker-registry`, `docker-namespace`, `checkout-path`. Declared outputs: `kibana-docker-image`, `kibana-commit-sha`, `kibana-stack-version`. |
| Outputs | No workflow/job outputs are declared. Step outputs referenced by name: `kibana-commit-sha, kibana-docker-image, kibana-stack-version`. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | `ELASTIC_DOCKER_PASSWORD`, `ELASTIC_DOCKER_REGISTRY`, `ELASTIC_DOCKER_USERNAME` |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-kibana-docker-image.yml`](../test-kibana-docker-image.yml#L1-78)
- Local action: [`kibana-docker-image/action.yml`](../../../kibana-docker-image/action.yml) and [`kibana-docker-image/README.md`](../../../kibana-docker-image/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
