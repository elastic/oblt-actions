# <!--name-->oblt-cli/setup<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Foblt-cli%2Fsetup+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)
[![test-oblt-cli-setup](https://github.com/elastic/oblt-actions/actions/workflows/test-oblt-cli-setup.yml/badge.svg?branch=main)](https://github.com/elastic/oblt-actions/actions/workflows/test-oblt-cli-setup.yml)

<!--description-->
Setup oblt-cli for use in GitHub Actions workflows.
<!--/description-->

> [!NOTE]
> This action does not provide a way to automatically download the latest version of `oblt-cli` to ensure that the used version is stable and the action is reproducible.
> If you don't provide both the `version` or `version-file` input, then the default version defined in [.default-oblt-cli-version](.default-oblt-cli-version) will be used.
> The default version will be updated by updatecli when a new version of `oblt-cli` is available. Only maintainers will decide to merge the PR created by updatecli to update the version.

## Inputs
<!--inputs-->
| Name             | Description                                                                                                        | Required | Default                 |
|------------------|--------------------------------------------------------------------------------------------------------------------|----------|-------------------------|
| `github-token`   | The GitHub access token.                                                                                           | `true`   | ` `                     |
| `slack-channel`  | The slack channel to notify the status.                                                                            | `false`  | `#observablt-bots`      |
| `username`       | Username to show in the deployments with oblt-cli, format: [a-z0-9]                                                | `false`  | `obltmachine`           |
| `version`        | Install a specific version of oblt-cli. If both `version` and `version-file` are provided, `version` will be used. | `false`  | ` `                     |
| `version-file`   | The file to read the version from. E.g. `.oblt-cli-version` or `.tool-versions` (asdf-vm).                         | `false`  | ` `                     |
| `gcp-project-id` | The GCP Project ID                                                                                                 | `false`  | `elastic-observability` |
<!--/inputs-->

## Usage
<!--usage action="elastic/oblt-actions/**" version="env:VERSION"-->
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
<!--/usage-->
