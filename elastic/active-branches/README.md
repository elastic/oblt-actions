# <!--name-->elastic/active-branches<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Felastic%2Factive-branches+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)
[![test-elastic-active-branches](https://github.com/elastic/oblt-actions/actions/workflows/test-elastic-active-branches.yml/badge.svg?branch=main)](https://github.com/elastic/oblt-actions/actions/workflows/test-elastic-active-branches.yml)

<!--description-->
Fetch the current list of active branches in Elastic (the ones based on the Unified Release process)
<!--/description-->

## Inputs
<!--inputs-->
| Name               | Description                      | Required | Default |
|--------------------|----------------------------------|----------|---------|
| `exclude-branches` | Exclude branches comma separated | `false`  | ` `     |
<!--/inputs-->

## Outputs

<!--outputs-->
| Name       | Description                                                   |
|------------|---------------------------------------------------------------|
| `matrix`   | Processed matrix with the branches (using the include format) |
| `branches` | Processed list of branches                                    |
<!--/outputs-->

## Usage

<!--usage action="elastic/oblt-actions/**" version="env:VERSION"-->
```yaml
jobs:
  filter:
    runs-on: ubuntu-latest
    timeout-minutes: 1
    outputs:
      matrix: ${{ steps.generator.outputs.matrix }}
    steps:
      - id: generator
        uses: elastic/oblt-actions/elastic/active-branches@v1
        with:
          exclude-branches: '7.17'

  bump-elastic-stack:
    runs-on: ubuntu-latest
    needs: [filter]
    strategy:
      matrix: ${{ fromJson(needs.filter.outputs.matrix) }}

      # ...
```
<!--/usage-->
