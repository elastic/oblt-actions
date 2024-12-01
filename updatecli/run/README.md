# <!--name-->updatecli/run<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Fupdatecli%2Frun+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)
[![test-updatecli-run](https://github.com/elastic/oblt-actions/actions/workflows/test-updatecli-run.yml/badge.svg?branch=main)](https://github.com/elastic/oblt-actions/actions/workflows/test-updatecli-run.yml)

## Inputs

<!--inputs-->
| Name           | Description                                                                                                         | Required | Default |
|----------------|---------------------------------------------------------------------------------------------------------------------|----------|---------|
| `command`      | Specify the updatecli command to be executed.                                                                       | `true`   | ` `     |
| `version`      | Install a specific version of updatecli. If both `version` and `version-file` are provided, `version` will be used. | `false`  | ` `     |
| `version-file` | The file to read the version from. E.g. `.updatecli-version` or `.tool-versions` (asdf-vm).                         | `false`  | ` `     |
<!--/inputs-->

## Usage

<!--usage action="elastic/oblt-actions/**" version="env:VERSION"-->
```yaml
name: updatecli

jobs:
  updatecli:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Install Updatecli in the runner
        uses: elastic/oblt-actions/updatecli/run@v1
        with:
          command: apply --config updatecli/updatecli.d
```
<!--/usage-->
