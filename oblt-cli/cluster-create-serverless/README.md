# <!--name-->oblt-cli/cluster-create-serverless<!--/name-->

[![test-oblt-cli-cluster-create-serverless](https://github.com/elastic/oblt-actions/actions/workflows/test-oblt-cli-cluster-create-serverless.yml/badge.svg?branch=main)](https://github.com/elastic/oblt-actions/actions/workflows/test-oblt-cli-cluster-create-serverless.yml)

<!--description-->
Run the oblt-cli wrapper to create a serverless cluster.
<!--/description-->

## Inputs
<!--inputs-->
| Name                  | Description                                                                  | Required | Default            |
|-----------------------|------------------------------------------------------------------------------|----------|--------------------|
| `cluster-name-prefix` | Prefix to be prepended to the randomised cluster name                        | `false`  | ` `                |
| `cluster-name-suffix` | Suffix to be appended to the randomised cluster name                         | `false`  | ` `                |
| `target`              | The target environment where to deploy the serverless cluster. Default: `qa` | `false`  | `qa`               |
| `project-type`        | The project type. Default: `observability`                                   | `false`  | `observability`    |
| `github-token`        | The GitHub access token.                                                     | `true`   | ` `                |
| `slack-channel`       | The slack channel to notify the status.                                      | `false`  | `#observablt-bots` |
| `username`            | Username to show in the deployments with oblt-cli, format: [a-z0-9]          | `false`  | `obltmachine`      |
| `gitops`              | Whether to provide the GitOps metadata to the oblt-cli                       | `false`  | `false`            |
| `dry-run`             | Whether to dryRun                                                            | `false`  | `false`            |
<!--/inputs-->

## Usage

<!--usage action="elastic/oblt-actions/oblt-cli/create-serverless" version="env:VERSION"-->
```yaml
jobs:
  create-serverless:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: elastic/oblt-actions/google/auth@v1
      - uses: elastic/oblt-actions/git/setup@v1
      - uses: elastic/oblt-actions/oblt-cli/create-serverless@v1
        with:
          target: 'staging'
          cluster-name-prefix: 'foo'
          github-token: ${{ secrets.PAT_TOKEN }}
```
<!--/usage-->
