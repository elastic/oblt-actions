# <!--name-->check-dependent-jobs<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Fcheck-dependent-jobs+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)
[![test-check-dependent-jobs](https://github.com/elastic/oblt-actions/actions/workflows/test-check-dependent-jobs.yml/badge.svg?branch=main)](https://github.com/elastic/oblt-actions/actions/workflows/test-check-dependent-jobs.yml)

<!--description-->
Evaluates the combined the status results of the provided needs context.
<!--/description-->

## Inputs
<!--inputs-->
| Name                 | Description                                    | Required | Default |
|----------------------|------------------------------------------------|----------|---------|
| `jobs`               | needs context as JSON string                   | `true`   | ` `     |
| `skipped-as-success` | Whether to consider skipped jobs as successful | `false`  | `false` |
<!--/inputs-->

## Outputs

<!--outputs-->
| Name         | Description                                                     |
|--------------|-----------------------------------------------------------------|
| `is-success` | The evaluated result of all provided jobs in the needs context. |
| `status`     | One of success or failure.                                      |
<!--/outputs-->

## Usage

<!--usage action="elastic/oblt-actions/**" version="env:VERSION"-->
```yaml
jobs:
  job-a:
    runs-on: ubuntu-latest
    steps:
      - run: exit 1;
  job-b:
    runs-on: ubuntu-latest
    steps:
      - run: exit 0;
  job-c:
    if: always()
    runs-on: ubuntu-latest
    needs:
      - job-a
      - job-b
    steps:
      - id: check
        uses: elastic/oblt-actions/check-dependent-jobs@v1
        with:
          jobs: ${{ toJSON(needs) }}
      - run: ${{ steps.check.outputs.is-success }} # should exit with 1 or 0.
```
<!--/usage-->
