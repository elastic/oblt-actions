# oblt-cli/run

GitHub Action to run the oblt-cli wrapper

## Inputs

| Name            | Description                                                          | Required | Default                     |
|-----------------|----------------------------------------------------------------------|----------|-----------------------------|
| `command`       | The oblt-cli command to run, without the oblt-cli prefix.            | `true`   |                             |
| `github-token`  | The GitHub token with permissions fetch releases.                    | `true`   |                             |
| `slack-channel` | The slack channel to be configured in the oblt-cli.                  | `false`  | `#observablt-bots`          |
| `username`      | Username to show in the deployments with oblt-cli, format: [a-z0-9]. | `false`  | `apmmachine`                |

## Usage

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
