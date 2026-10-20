# test-aws-auth

Test workflow for `aws-auth`. This is an opinionated GitHub Action to authenticate with AWS. It generates a role ARN based on the repository name and the workflow filename, which is compatible with the AWS role ARN we use for Elastic Observability repositories.

## At a glance

| | |
| --- | --- |
| Platform | GitHub Actions |
| Source | [`test-aws-auth.yml`](../test-aws-auth.yml#L1-L29) |
| Trigger | `merge_group`; `workflow_dispatch`; `pull_request` (paths: `aws/auth/**, .github/workflows/test-aws-auth.yml`); `push` (branches: `main`; paths: `aws/auth/**, .github/workflows/test-aws-auth.yml`) |

## Purpose

Test workflow for `aws-auth`. This is an opinionated GitHub Action to authenticate with AWS. It generates a role ARN based on the repository name and the workflow filename, which is compatible with the AWS role ARN we use for Elastic Observability repositories.

Repository guidance says dedicated `test-<action>.yml` workflows provide the required `test` status check and exercise composite actions through `uses: ./<action-path>`.
See [CONTRIBUTING.md](../../../docs/CONTRIBUTING.md) for the repository guidance.

## When it runs

The workflow-level trigger is `merge_group`; `workflow_dispatch`; `pull_request` (paths: `aws/auth/**, .github/workflows/test-aws-auth.yml`); `push` (branches: `main`; paths: `aws/auth/**, .github/workflows/test-aws-auth.yml`). Conditions below can further restrict individual jobs or steps.

## Execution flow

| Job | Runner / reusable workflow | Depends on | Condition | Matrix |
| --- | --- | --- | --- | --- |
| `test` | `ubuntu-latest` | None declared | `Default GitHub condition` | `—` |

### `test` steps

| Order | Step | Action / command | Condition | Inputs / environment |
| ---: | --- | --- | --- | --- |
| 1 | Step 1 | `actions/checkout@v7` | `—` | — |
| 2 | Step 2 | `./aws/auth` | `—` | `aws-region` |
| 3 | Step 3 | `aws sts get-caller-identity` | `—` | — |

## Inputs, outputs, and access

| Item | Details |
| --- | --- |
| Workflow inputs | No `workflow_dispatch` inputs are declared. |
| Permissions | Workflow: `contents: read, id-token: write`; job overrides: `none`. |
| Local actions | [`aws/auth/action.yml`](../../../aws/auth/action.yml); [usage README](../../../aws/auth/README.md) — This is an opinionated GitHub Action to authenticate with AWS. It generates a role ARN based on the repository name and the workflow filename, which is compatible with the AWS role ARN we use for Elastic Observability repositories. Inputs: `aws-account-id`, `aws-region`, `role-duration-seconds`, `output-credentials`. Declared outputs: `role-arn`, `aws-account-id`, `aws-access-key-id`, `aws-secret-access-key`, `aws-session-token`. |
| Outputs | No workflow/job outputs are declared. |
| Artifacts and caches | No GitHub artifact-upload/download or cache action is declared directly in this workflow. |
| Secrets | No `secrets.*` references found in the workflow source. |

## Operational notes

This is a test workflow, not a deployment/release pipeline. Its action behavior is exercised by the local `uses:` references above; test commands/assertions are shown in step order.
Only settings and references declared in the checked-in source are documented; repository/organization-level settings and remote action implementations are outside this source.

## Sources and history

- Workflow: [`test-aws-auth.yml`](../test-aws-auth.yml#L1-29)
- Local action: [`aws/auth/action.yml`](../../../aws/auth/action.yml) and [`aws/auth/README.md`](../../../aws/auth/README.md)
- Rationale: [`CONTRIBUTING.md`](../../../docs/CONTRIBUTING.md)
