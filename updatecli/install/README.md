# <!--name-->updatecli/install<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Fupdatecli%2Finstall+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)

<!--description-->
This is an opinionated GitHub Action to install the updatecli
<!--/description-->

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
        uses: elastic/oblt-actions/updatecli/install@v1
```
<!--/usage-->
