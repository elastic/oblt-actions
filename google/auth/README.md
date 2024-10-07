# <!--name-->google/auth<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Fgoogle%2Fauth+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)
[![test-google-auth](https://github.com/elastic/oblt-actions/actions/workflows/test-google-auth.yml/badge.svg?branch=main)](https://github.com/elastic/oblt-actions/actions/workflows/test-google-auth.yml)

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
| `project-id`     | The GCP project ID     | `false`  | `elastic-observability`    |
| `repository`     | The repository name    | `false`  | `${{ github.repository }}` |
<!--/inputs-->

## Outputs
<!--outputs-->
| Name                         | Description                                      |
|------------------------------|--------------------------------------------------|
| `workload-identity-provider` | The generated Workload Identity Pool Provider ID |
<!--/outputs-->

## Usage

<!--usage action="elastic/oblt-actions/**" version="env:VERSION"-->
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
<!--/usage-->
