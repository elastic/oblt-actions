# <!--name-->version-framework<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Fversion-framework+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)

<!--description-->
Create matrix for the supported versions and frameworks
<!--/description-->

## Inputs

<!--inputs-->
| Name              | Description                                                                                               | Required | Default |
|-------------------|-----------------------------------------------------------------------------------------------------------|----------|---------|
| `versions-file`   | The YAML file with the versions. Being VERSION the key for the list                                       | `true`   | ` `     |
| `frameworks-file` | The YAML file with the frameworks. Being FRAMEWORK the key for the list                                   | `true`   | ` `     |
| `excluded-file`   | The YAML file with the excluded tuples. Being exclude the key for the list of tuples (VERSION, FRAMEWORK) | `false`  | ` `     |
<!--/inputs-->

## Outputs

<!--outputs-->
| Name     | Description                                                        |
|----------|--------------------------------------------------------------------|
| `matrix` | Processed matrix with the required tuples of version and framework |
<!--/outputs-->

## Usage

<!--usage action="elastic/oblt-actions/**" version="env:VERSION"-->
```yaml
on:
  push:

permissions:
  contents: read

jobs:
  create-test-matrix:
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.generate.outputs.matrix }}
    steps:
      - uses: actions/checkout@v4
      - id: generate
        uses: elastic/oblt-actions/version-framework@v1
        with:
          versions-file: .ci/.ruby.yml
          frameworks-file: .ci/.main_framework.yml
          excluded-file: .ci/.exclude.yml

  test:
    needs:
      - create-test-matrix
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      max-parallel: 20
      matrix: ${{ fromJSON(needs.create-test-matrix.outputs.matrix) }}
    steps:
      - uses: actions/checkout@v4
      [..]
```
<!--/usage-->
