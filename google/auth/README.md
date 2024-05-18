# google/auth

This is an opinionated GitHub Action to authenticate with GCP.
It generates a Workload Identity Pool Provider ID based on the repository name, which is compatible with the
GCP Workload Identity Pool Provider ID we use for Elastic Observability repositories.

## Usage

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
