# <!--name-->feature-freeze<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Ffeature-freeze+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)
[![test-feature-freeze](https://github.com/elastic/oblt-actions/actions/workflows/test-feature-freeze.yml/badge.svg?branch=main)](https://github.com/elastic/oblt-actions/actions/workflows/test-feature-freeze.yml)

<!--description-->
An Action to check if a repository is currently in a feature freeze period.
<!--/description-->

## Inputs

<!--inputs-->
| Name                  | Description                                                       | Required | Default                    |
|-----------------------|-------------------------------------------------------------------|----------|----------------------------|
| `github-repository`   | The GitHub repository (format: ORG/REPO)                          | `false`  | `${{ github.repository }}` |
| `git-ref`             | The git ref of the repository to check. (Default: default branch) | `false`  | ` `                        |
| `feature-freeze-file` | The path to the feature freeze file.                              | `false`  | `release-freezes.json`     |
<!--/inputs-->

## Outputs

<!--outputs-->
| Name        | Description                                           |
|-------------|-------------------------------------------------------|
| `in-freeze` | Whether the repository is in a feature freeze period. |
<!--/outputs-->

## Usage

<!--usage action="elastic/oblt-actions/**" version="env:VERSION"-->
```yaml
---
name: example

on: workflow_dispatch

jobs:
  check-feature-freeze:
    runs-on: ubuntu-latest
    outputs:
      in-freeze: ${{ steps.feature-freeze.outputs.in-freeze }}
    steps:
      - uses: 'elastic/oblt-actions/feature-freeze@v1'
        id: feature-freeze

  create-release-tag:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    needs: [check-feature-freeze]
    if: needs.check-feature-freeze.outputs.in-freeze == 'false'
    ...

```
<!--/usage-->
