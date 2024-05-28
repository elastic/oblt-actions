# oblt-cli/setup

Setup oblt-cli for use in GitHub Actions workflows. Only works in conjunction with the [google/auth](../../google/auth) action
because it's required to authenticate with the Google Cloud Platform to access the OBLT cluster secrets

## Inputs

| name            | Description                                                          | required | default            |
|-----------------|----------------------------------------------------------------------|----------|--------------------|
| `github-token`  | The GitHub token with permissions fetch releases.                    | `true`   |                    |
| `slack-channel` | The slack channel to be configured in the oblt-cli.                  | `false`  | `#observablt-bots` |
| `username`      | Username to show in the deployments with oblt-cli, format: [a-z0-9]. | `false`  | `obltmachine`      |
| `version`       | Install a specific version of oblt-cli. Latest version if empty.     | `false`  | `""`               |


## Usage


```yaml
jobs:
  run-oblt-cli:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: elastic/oblt-actions/google-auth@v1
      - uses: elastic/oblt-actions/git/setup@v1
      - uses: elastic/oblt-actions/oblt-cli/setup@v1
        with:
          github-token: ${{ secrets.PAT }}
      - run: oblt-cli cluster list
```
