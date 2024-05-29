# oblt-cli/cluster-create-serverless

GitHub Action to run the oblt-cli wrapper to create a Serverless cluster

## Inputs

Following inputs can be used as `step.with` keys

| Name                  | Description                                                          | Required  | Default            |
|-----------------------|----------------------------------------------------------------------|-----------|--------------------|
| `target`              | The target environment where to deploy the serverless cluster.       | `false`   | `qa`               |
| `project-type`        | The project type.                                                    | `false`   | `observability`    |
| `cluster-name-prefix` | Prefix to be prepended to the randomised cluster name                | `false`   | ` `                |
| `cluster-name-suffix` | Suffix to be appended to the randomised cluster name                 | `false`   | ` `                |
| `dry-run`             | Whether to dry-run the oblt-cli.                                     | `false`   | `false`            |
| `slack-channel`       | The slack channel to be configured in the oblt-cli.                  | `false`   | `#observablt-bots` |
| `github-token`        | The GitHub token with permissions fetch releases.                    | `true`    | ` `                |
| `username`            | Username to show in the deployments with oblt-cli, format: [a-z0-9]. | `false`   | `apmmachine`       |
| `gitops`              | Whether to provide the GitOps metadata to the oblt-cli.              | `false`   | `false`            |

## Usage

```yaml
jobs:
  create-serverless:
    runs-on: ubuntu-latest
    steps:
      - uses: elastic/oblt-actions/oblt-cli/create-serverless@v1
        with:
          target: 'staging'
          cluster-name-prefix: 'foo'
          github-token: ${{ secrets.PAT_TOKEN }}
```
