# <!--name-->oblt-cli/run<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Foblt-cli%2Frun+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)
[![test-oblt-cli-run](https://github.com/elastic/oblt-actions/actions/workflows/test-oblt-cli-run.yml/badge.svg?branch=main)](https://github.com/elastic/oblt-actions/actions/workflows/test-oblt-cli-run.yml)

<!--description-->
Run the oblt-cli wrapper.
<!--/description-->

## Inputs
<!--inputs-->
| Name             | Description                                                         | Required | Default                 |
|------------------|---------------------------------------------------------------------|----------|-------------------------|
| `command`        | The oblt-cli command to run                                         | `true`   | ` `                     |
| `github-token`   | The GitHub access token.                                            | `true`   | ` `                     |
| `slack-channel`  | The slack channel to notify the status.                             | `false`  | `#observablt-bots`      |
| `username`       | Username to show in the deployments with oblt-cli, format: [a-z0-9] | `false`  | `obltmachine`           |
| `gcp-project-id` | The GCP Project ID                                                  | `false`  | `elastic-observability` |
<!--/inputs-->

## Usage
<!--usage action="elastic/oblt-actions/**" version="env:VERSION"-->
```yaml
jobs:
  run-oblt-cli:
    runs-on: ubuntu-latest
    steps:
      - uses: elastic/oblt-actions/oblt-cli/run@v1
        with:
          command: 'cluster create ccs --remote-cluster=dev-oblt --cluster-name-prefix mycustomcluster'
          github-token: ${{ secrets.PAT_TOKEN }}
```
<!--/usage-->
