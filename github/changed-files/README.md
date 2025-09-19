# <!--name-->changed-files<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Fgithub%2Fchanged-files+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)
[![test-github-changed-files](https://github.com/elastic/oblt-actions/actions/workflows/test-github-changed-files.yml/badge.svg?branch=main)](https://github.com/elastic/oblt-actions/actions/workflows/test-github-changed-files.yml)

<!--description-->
Check the files changed between two git references.
It uses the `git diff` command to get the files changed between two git references.
It can filter the files based on the file extension.
The code is based on the [git-changed-files](https://github.com/kandhavivekraj/git-changed-files) with minimal changes.
<!--/description-->

## Inputs
<!--inputs-->
| Name       | Description                                                                          | Required | Default               |
|------------|--------------------------------------------------------------------------------------|----------|-----------------------|
| `base-ref` | The base ref to compare the changes. (default: github.sha^1)                         | `false`  | `${{ github.sha }}^1` |
| `ref`      | The ref to compare the changes. (default: github.sha)                                | `false`  | `${{ github.sha }}`   |
| `filter`   | The JSON filter to apply to the changes. (default '["*.*"]') '["*/*.yaml","*.json"]' | `false`  | `["*.*"]`             |
<!--/inputs-->

## Outputs
<!--outputs-->
| Name             | Description                                         |
|------------------|-----------------------------------------------------|
| `deleted`        | The JSON list of deleted files.                     |
| `modified`       | The JSON list of modified files.                    |
| `added`          | The JSON list of added files.                       |
| `changed`        | The JSON list of added, modified and deleted files. |
| `count`          | The count of files.                                 |
| `count-deleted`  | The count of deleted files.                         |
| `count-modified` | The count of modified files.                        |
| `count-added`    | The count of added files.                           |
<!--/outputs-->

## Usage

<!--usage action="elastic/oblt-actions/**" version="env:VERSION"-->
```yaml
name: Check files changed in PR
on:
  pull_request:
jobs:
  filter-files:
    runs-on: ubuntu-latest
    steps:
      - uses: elastic/oblt-actions/github/changed-files
        id: changed-files
        with:
          base-ref: "origin/main"
          ref: ${{ github.sha }}
          filter: '["*.yaml","*.json", "*folder/folder/*/file.json"]'
      - name: test count
        if: ${{ steps.changed-files.outputs.count > 0}}
        run: |
          echo "count=${{ steps.changed-files.outputs.count }}"
          echo "count-deleted=${{ steps.changed-files.outputs.count-deleted }}"
          echo "count-added=${{ steps.changed-files.outputs.count-added }}"
          echo "count-modified=${{ steps.changed-files.outputs.count-modified }}"
```
<!--/usage-->
