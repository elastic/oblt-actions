# <!--name-->elastic/github-commands<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Felastic%2Fgithub-commands+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)
[![test-elastic-github-commands](https://github.com/elastic/oblt-actions/actions/workflows/test-elastic-github-commands.yml/badge.svg?branch=main)](https://github.com/elastic/oblt-actions/actions/workflows/test-elastic-github-commands.yml)

<!--description-->
Print the supported GitHub commands
<!--/description-->

## Inputs
<!--inputs-->
| Name                | Description                   | Required | Default               |
|---------------------|-------------------------------|----------|-----------------------|
| `github-token`      | The GitHub access token.      | `false`  | `${{ github.token }}` |
| `continue-on-error` | Whether to continue on error. | `false`  | `true`                |
<!--/inputs-->

## Outputs

<!--outputs-->
| Name | Description |
|------|-------------|
<!--/outputs-->

## Usage

<!--usage action="elastic/oblt-actions/**" version="env:VERSION"-->
```yaml
---
name: github-commands-comment

on:
  pull_request_target:
    types:
      - opened

permissions:
  contents: read

jobs:
  comment:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
    steps:
      - uses: elastic/oblt-actions/elastic/github-commands@v1

```

<!--/usage-->
