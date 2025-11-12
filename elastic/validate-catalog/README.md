# <!--name-->elastic/validate-catalog<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Felastic%2Fvalidate-catalog+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)
[![test-elastic-validate-catalog](https://github.com/elastic/oblt-actions/actions/workflows/test-elastic-validate-catalog.yml/badge.svg?branch=main)](https://github.com/elastic/oblt-actions/actions/workflows/test-elastic-validate-catalog.yml)

<!--description-->
Run the catalog-info validation
<!--/description-->

## Inputs
<!--inputs-->
| Name              | Description                       | Required | Default                                                               |
|-------------------|-----------------------------------|----------|-----------------------------------------------------------------------|
| `container-image` | The catalog info container image. | `false`  | `ghcr.io/elastic/observability-robots/ci-agent-images/pipelib:latest` |
| `github-token`    | The GitHub access token.          | `false`  | `${{ github.token }}`                                                 |
<!--/inputs-->

## Outputs

<!--outputs-->
| Name | Description |
|------|-------------|
<!--/outputs-->

## Usage

You need to grant the read access to the container image called [pipelib](https://github.com/orgs/elastic/packages?tab=packages&q=pipelib). It's not public available but granted to individual GitHub repositories.


<!--usage action="elastic/oblt-actions/**" version="env:VERSION"-->
```yaml
---
name: catalog-info

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main
    paths:
      - 'catalog-info.yaml'

permissions:
  contents: read

jobs:
  validate:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: read
    steps:
      - uses: actions/checkout@v5
      - uses: elastic/oblt-actions/elastic/validate-catalog@v1
```
<!--/usage-->
