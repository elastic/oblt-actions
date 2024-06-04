# <!--name-->oblt-cli/cluster-create-ccs<!--/name-->
<!--description-->
Run the oblt-cli wrapper to create a CCS cluster.
<!--/description-->

## Inputs
<!--inputs-->
| Name                         | Description                                                         | Required | Default            |
|------------------------------|---------------------------------------------------------------------|----------|--------------------|
| `remote-cluster`             | The Oblt cluster to use                                             | `true`   | ` `                |
| `github-token`               | The GitHub access token.                                            | `true`   | ` `                |
| `cluster-name-prefix`        | Prefix to be prepended to the randomised cluster name               | `false`  | ` `                |
| `cluster-name-suffix`        | Suffix to be appended to the randomised cluster name                | `false`  | ` `                |
| `elasticsearch-docker-image` | Force to use a Docker image for the Elasticsearch Deployment        | `false`  | ` `                |
| `slack-channel`              | The slack channel to notify the status.                             | `false`  | `#observablt-bots` |
| `username`                   | Username to show in the deployments with oblt-cli, format: [a-z0-9] | `false`  | `obltmachine`      |
| `gitops`                     | Whether to provide the GitOps metadata to the oblt-cli              | `false`  | `false`            |
| `dry-run`                    | Whether to dryRun                                                   | `false`  | `false`            |
<!--/inputs-->

## Usage
<!--usage action="elastic/oblt-actions/oblt-cli/cluster-create-ccs" version="env:VERSION"-->
```yaml
jobs:
  run-oblt-cli:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: elastic/oblt-actions/git/setup@v1
      - uses: elastic/oblt-actions/google/auth@v1
      - uses: elastic/oblt-actions/oblt-cli/cluster-create-ccs@v1
        with:
          remote-cluster: 'dev-oblt'
          cluster-name-prefix: 'foo'
          github-token: ${{ secrets.PAT_TOKEN }}
```
<!--/usage-->
