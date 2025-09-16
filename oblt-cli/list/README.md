# <!--name-->oblt-cli/list<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Foblt-cli%list+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)
[![test-oblt-cli-list](https://github.com/elastic/oblt-actions/actions/workflows/test-oblt-cli-list.yml/badge.svg?branch=main)](https://github.com/elastic/oblt-actions/actions/workflows/test-oblt-cli-list.yml)

<!--description-->
List clusters using a filter
<!--/description-->

## Inputs
<!--inputs-->
| Name            | Description                                                                            | Required | Default            |
|-----------------|----------------------------------------------------------------------------------------|----------|--------------------|
| `github-token`  | The GitHub access token.                                                               | `true`   | ` `                |
| `slack-channel` | The slack channel to notify the status.                                                | `false`  | `#observablt-bots` |
| `username`      | Username to show in the deployments with oblt-cli, format: [a-z0-9]                    | `false`  | `obltmachine`      |
| `version`       | The oblt-cli version to use.                                                           | `false`  | ` `                |
| `verbose`       | Run oblt-cli in verbose mode.                                                          | `false`  | `false`            |
| `filter-key`    | The filter key to use.                                                                 | `false`  | ` `                |
| `filter-value`  | The filter value to use.                                                               | `false`  | ` `                |
| `all`           | List all clusters.                                                                     | `false`  | `false`            |
| `fail-on-empty` | Fail the action if no clusters are found.                                              | `false`  | `false`            |
| `save-to-file`  | File path to save the output to.                                                       | `false`  | `clusters.json`    |
| `version-file`  | File containing the oblt-cli version to use. If set, this overrides the version input. | `false`  | ` `                |
<!--/inputs-->

## Usage
<!--usage action="elastic/oblt-actions/**" version="env:VERSION"-->
```yaml
jobs:
  run-oblt-cli:
    runs-on: ubuntu-latest
    steps:
      - uses: elastic/oblt-actions/oblt-cli/list@v1
        with:
          filter-key: "stack.update_schedule"
          filter-value: "monday"
          save-to-file: "${{ github.workspace }}/updates.json"
          verbose: 'true'
          all: 'true'
          github-token: ${{ secrets.PAT_TOKEN }}
```
<!--/usage-->
