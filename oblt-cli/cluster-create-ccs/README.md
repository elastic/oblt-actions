# oblt-cli/cluster-create-ccs
Run the oblt-cli wrapper to create a CCS cluster.

## Inputs
| Name                         | Description                                                         | Required | Default            |
|------------------------------|---------------------------------------------------------------------|----------|--------------------|
| `remote-cluster`             | The Oblt cluster to use                                             | `true`   | ` `                |
| `github-token`               | The GitHub access token.                                            | `true`   | ` `                |
| `cluster-name-prefix`        | Prefix to be prepended to the randomised cluster name               | `false`  | ` `                |
| `cluster-name-suffix`        | Suffix to be appended to the randomised cluster name                | `false`  | ` `                |
| `elasticsearch-docker-image` | Force to use a Docker image for the Elasticserach Deployment        | `false`  | ` `                |
| `slack-channel`              | The slack channel to notify the status.                             | `false`  | `#observablt-bots` |
| `username`                   | Username to show in the deployments with oblt-cli, format: [a-z0-9] | `false`  | `apmmachine`       |
| `gitops`                     | Whether to provide the GitOps metadata to the oblt-cli              | `false`  | `false`            |
| `dry-run`                    | Whether to dryRun                                                   | `false`  | `false`            |

## Usage

```yaml
---
name: Create ccs cluster using the oblt-cli
on:
  issues:
    types: [opened]
jobs:
  run-oblt-cli:
    runs-on: ubuntu-latest
    steps:
      - uses: elastic/oblt-actions/oblt-cli/cluster-create-ccs@v1
        with:
          remote-cluster: 'dev-oblt'
          cluster-name-prefix: 'foo'
          github-token: ${{ secrets.PAT_TOKEN }}
```
