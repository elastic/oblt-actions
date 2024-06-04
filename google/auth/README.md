# <!--name-->google/auth<!--/name-->

<!--description-->
This is an opinionated GitHub Action to authenticate with GCP.
It generates a Workload Identity Pool Provider ID based on the repository name, which is compatible with the
GCP Workload Identity Pool Provider ID we use for Elastic Observability repositories.
<!--/description-->

## Inputs

<!--inputs-->
| Name             | Description            | Required | Default                    |
|------------------|------------------------|----------|----------------------------|
| `project-number` | The GCP project number | `false`  | `8560181848`               |
| `repository`     | The repository name    | `false`  | `${{ github.repository }}` |
<!--/inputs-->

## Outputs
<!--outputs-->
| Name                         | Description                                      |
|------------------------------|--------------------------------------------------|
| `workload-identity-provider` | The generated Workload Identity Pool Provider ID |
<!--/outputs-->

## Usage

<!--usage action="elastic/oblt-actions/google/auth" version="env:VERSION"-->
```yaml
jobs:
  job_id:
    permissions:
      contents: 'read'
      id-token: 'write'
    steps:
      - uses: 'actions/checkout@v4' # Checkout needs to happen before using this action
      - uses: 'elastic/oblt-actions/google/auth@v1'
```
<--/usage-->
