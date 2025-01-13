# <!--name-->github/labels-copier<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2F2Fmergify%labels-copier+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)
[![test-mergify-labels-copier](https://github.com/elastic/oblt-actions/actions/workflows/test-github-comment-reaction.yml/badge.svg?branch=main)](https://github.com/elastic/oblt-actions/actions/workflows/test-mergify-labels-copier.yml)

<!--description-->
copies pull request labels to backported PRs
<!--/description-->

## Inputs
<!--inputs-->
| Name                    | Description                                     | Required | Default                                   |
|-------------------------|-------------------------------------------------|----------|-------------------------------------------|
| `excluded-labels-regex` | labels to be excluded in regex format           | `false`  | ` `                                       |
| `github-token`          | The GitHub token to use for API requests        | `false`  | `${{ github.token }}`                     |
| `repository`            | The GitHub repository to use for API requests   | `false`  | `${{ github.repository }}`                |
| `pull-request`          | The GitHub pull-request to use for API requests | `false`  | `${{ github.event.pull_request.number }}` |
<!--/inputs-->

## Outputs
<!--outputs-->
| Name     | Description             |
|----------|-------------------------|
| `labels` | The labels to be copied |
<!--/outputs-->

## Usage

<!--usage action="elastic/oblt-actions/**" version="env:VERSION"-->
```yaml
name: mergify backport labels copier

on:
  pull_request:
    types:
      - opened
jobs:
  react:
    runs-on: ubuntu-latest
    if: startsWith(github.head_ref, 'mergify/bp/')
    permissions:
      # Add GH labels
      pull-requests: write
      # See https://github.com/cli/cli/issues/6274
      repository-projects: read
    steps:
      - uses: elastic/oblt-actions/mergify/labels-copier@v1
        with:
          excluded-labels-regex: "^backport-*"
      # ...
```
<!--/usage-->
