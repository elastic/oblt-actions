# <!--name-->oblt/cli/cluster-destroy<!--/name-->
<!--description-->
Run the oblt-cli wrapper to destroy the given cluster
<!--/description-->

## Inputs
<!--inputs-->
| Name                | Description                                                         | Required | Default       |
|---------------------|---------------------------------------------------------------------|----------|---------------|
| `cluster-name`      | The cluster name                                                    | `false`  | ` `           |
| `cluster-info-file` | The cluster info file (absolute path)                               | `false`  | ` `           |
| `github-token`      | The GitHub access token.                                            | `true`   | ` `           |
| `username`          | Username to show in the deployments with oblt-cli, format: [a-z0-9] | `false`  | `obltmachine` |
<!--/inputs-->

## Usage
<!--usage action="elastic/oblt-actions/oblt-cli/cluster-destroy" version="env:VERSION"-->
```yaml
jobs:
  destroy-oblt-cluster:
    runs-on: ubuntu-latest
    steps:
      - uses: elastic/oblt-actions/git/setup@v1
      - uses: elastic/oblt-actions/oblt-cli/cluster-destroy@v1
        with:
          cluster-name: 'foo'
          github-token: ${{ secrets.PAT_TOKEN }}
        if: always()
```
<!--/usage-->
