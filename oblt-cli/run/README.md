# <!--name-->oblt-cli/run<!--/name-->

[![test-oblt-cli-run](https://github.com/elastic/oblt-actions/actions/workflows/test-oblt-cli-run.yml/badge.svg?branch=main)](https://github.com/elastic/oblt-actions/actions/workflows/test-oblt-cli-run.yml)

<!--description-->
Run the oblt-cli wrapper.
<!--/description-->

## Inputs
<!--inputs-->
| Name            | Description                                                         | Required | Default            |
|-----------------|---------------------------------------------------------------------|----------|--------------------|
| `command`       | The oblt-cli command to run                                         | `true`   | ` `                |
| `github-token`  | The GitHub access token.                                            | `true`   | ` `                |
| `slack-channel` | The slack channel to notify the status.                             | `false`  | `#observablt-bots` |
| `username`      | Username to show in the deployments with oblt-cli, format: [a-z0-9] | `false`  | `obltmachine`      |
<!--/inputs-->

## Usage
<!--usage action="elastic/oblt-actions/oblt-cli/run" version="env:VERSION"-->
```yaml
jobs:
  run-oblt-cli:
    runs-on: ubuntu-latest
    steps:
      - uses: elastic/oblt-actions/oblt-cli/run@v1
        with:
          command: 'cluster create ccs --remote-cluster=dev-oblt --cluster-name-prefix mycustomcluster'
          token: ${{ secrets.PAT_TOKEN }}
```
<!--/usage-->
