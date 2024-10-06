# <!--name-->oblt-cli/undeploy-my-kibana<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Foblt-cli%2Fundeploy-my-kibana+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)
[![test-oblt-cli-cluster-name-validation](https://github.com/elastic/oblt-actions/actions/workflows/test-oblt-cli-undeploy-my-kibana.yml/badge.svg?branch=main)](https://github.com/elastic/oblt-actions/actions/workflows/test-oblt-cli-undeploy-my-kibana.yml)

<!--description-->
Undeploy my kibana given the Pull Request
<!--/description-->

## Inputs
<!--inputs-->
| Name           | Description                | Required | Default                                   |
|----------------|----------------------------|----------|-------------------------------------------|
| `pull-request` | The GitHub Pull Request ID | `false`  | `${{ github.event.pull_request.number }}` |
| `repository`   | The GitHub repository      | `false`  | `${{ github.repository }}`                |
| `github-token` | The GitHub access token.   | `true`   | ` `                                       |
<!--/inputs-->

## Outputs
<!--outputs-->
| Name    | Description                                                   |
|---------|---------------------------------------------------------------|
| `issue` | The GitHub issue that has been created to destroy the cluster |
<!--/outputs-->

## Usage
<!--usage action="elastic/oblt-actions/**" version="env:VERSION"-->
```yaml
name: undeploy-my-kibana

on:
  pull_request_target:
    types: [closed]

permissions:
  contents: read

jobs:
  undeploy-my-kibana:
    runs-on: ubuntu-latest
    steps:
      - uses: elastic/oblt-actions/oblt-cli/undeploy-my-kibana@v1
        with:
          github-token: ${{ secrets.PAT_TOKEN }}

```
<!--/usage-->
