# <!--name-->pre-commit<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Fpre-commit+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)
[![test-pre-commit](https://github.com/elastic/oblt-actions/actions/workflows/test-pre-commit.yml/badge.svg?branch=main)](https://github.com/elastic/oblt-actions/actions/workflows/test-pre-commit.yml)


<!--description-->
Run pre-commit independently you are running on a PR or a branch.
<!--/description-->

## Inputs

<!--inputs-->
| Name             | Description                                                                   | Required | Default |
|------------------|-------------------------------------------------------------------------------|----------|---------|
| `clean-checkout` | Whether to execute `git clean -ffdx && git reset --hard HEAD` before fetching | `false`  | `true`  |
| `python-version` | What Python version to use                                                    | `false`  | `3.11`  |
<!--/inputs-->

## Usage

<!--usage action="elastic/oblt-actions/**" version="env:VERSION"-->
```yaml
on:
  pull_request: ~

permissions:
  contents: read

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: elastic/oblt-actions/pre-commit@v1
```
<!--/usage-->
