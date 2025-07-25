# <!--name-->oblt-cli/cluster-create-custom<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Foblt-cli%2Fcluster-create-custom+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)
[![test-oblt-cli-cluster-create-custom](https://github.com/elastic/oblt-actions/actions/workflows/test-oblt-cli-cluster-create-custom.yml/badge.svg?branch=main)](https://github.com/elastic/oblt-actions/actions/workflows/test-oblt-cli-cluster-create-custom.yml)

<!--description-->
Run the oblt-cli wrapper to create a custom cluster.
<!--/description-->

## Inputs
<!--inputs-->
| Name                  | Description                                                                             | Required | Default            |
|-----------------------|-----------------------------------------------------------------------------------------|----------|--------------------|
| `template`            | The Oblt cluster template to use                                                        | `true`   | ` `                |
| `parameters`          | The Oblt cluster parameters to use in JSON format.                                      | `true`   | `{}`               |
| `github-token`        | The GitHub access token.                                                                | `true`   | ` `                |
| `cluster-name-prefix` | Prefix to be prepended to the randomised cluster name                                   | `false`  | ` `                |
| `cluster-name-suffix` | Suffix to be appended to the randomised cluster name                                    | `false`  | ` `                |
| `slack-channel`       | The slack channel to notify the status.                                                 | `false`  | `#observablt-bots` |
| `username`            | Username to show in the deployments with oblt-cli, format: [a-z0-9]                     | `false`  | `obltmachine`      |
| `gitops`              | Whether to provide the GitOps metadata to the oblt-cli                                  | `false`  | `false`            |
| `dry-run`             | Whether to dryRun                                                                       | `false`  | `false`            |
| `skip-random-name`    | Whether to deploy a cluster with a random name                                          | `false`  | `false`            |
| `wait`                | it waits N minutes for the operation to finish. (default 0 if no wait time is provided) | `false`  | `0`                |
<!--/inputs-->

## Outputs
<!--outputs-->
| Name           | Description                            |
|----------------|----------------------------------------|
| `cluster-name` | The cluster name that has been created |
<!--/outputs-->

## Usage
<!--usage action="elastic/oblt-actions/**" version="env:VERSION"-->
```yaml
---
name: Create custom cluster using the oblt-cli
on:
  issues:
    types: [opened]
jobs:
  run-oblt-cli:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: elastic/oblt-actions/git/setup@v1
      - uses: elastic/oblt-actions/oblt-cli/cluster-create-custom@v1
        with:
          template: 'deploy-kibana'
          cluster-name-prefix: 'foo'
          parameters: '{"RemoteClusterName":"release-oblt","StackVersion":"8.7.0","ElasticsearchDockerImage":"docker.elastic.co/observability-ci/elasticsearch-cloud-ess:8.7.0-046d305b","KibanaDockerImage":"docker.elastic.co/observability-ci/kibana-cloud:8.7.0-SNAPSHOT-87"}'
          github-token: ${{ secrets.PAT_TOKEN }}
```
<!--/usage-->
