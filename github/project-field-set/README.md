# <!--name-->github/project-field-set<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Fgithub%2Fproject-field-set+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)
[![test-github-project-field-set](https://github.com/elastic/oblt-actions/actions/workflows/test-github-project-field-set.yml/badge.svg?branch=main)](https://github.com/elastic/oblt-actions/actions/workflows/test-github-project-field-set.yml)

<!--description-->
Sets field of an GitHub project item
<!--/description-->

## Inputs
<!--inputs-->
| Name           | Description                                                                                                 | Required | Default               |
|----------------|-------------------------------------------------------------------------------------------------------------|----------|-----------------------|
| `github-token` | The GitHub access token.                                                                                    | `true`   | `${{ github.token }}` |
| `github-org`   | The GitHub org                                                                                              | `true`   | `elastic`             |
| `project-id`   | The GitHub project numeric ID.                                                                              | `true`   | ` `                   |
| `item-id`      | ID of item in the project                                                                                   | `true`   | ` `                   |
| `field-name`   | Field name                                                                                                  | `true`   | ` `                   |
| `field-value`  | Field value, when `field-type` = `iteration` then `@current` and `@next` and `@previous` are also supported | `true`   | ` `                   |
| `field-type`   | Field type, supported values are `single-select` and `iteration`                                            | `true`   | `single-select`       |
<!--/inputs-->

## Usage
<!--usage action="elastic/oblt-actions/github/project-field-set" version="env:VERSION"-->

```yaml
steps:
  # set single-select field
  - name: set status in project
    uses: elastic/oblt-actions/github/project-field-set@v1
    with:
      github-token: <GITHUB_TOKEN>
      github-org: 'elastic'
      project-id: 123456
      # <ITEM_ID> is provided by the `elastic/oblt-actions/github/project-add` action.
      item-id: <ITEM_ID>
      field-name: 'Status'
      field-value: 'In Progress'

  # set iteration field
  - name: set current iteration in project
    uses: elastic/oblt-actions/github/project-field-set@v1
    with:
      github-token: <GITHUB_TOKEN>
      github-org: 'elastic'
      project-id: 123456
      # <ITEM_ID> is provided by the `elastic/oblt-actions/github/project-add` action.
      item-id: <ITEM_ID>
      field-type: 'iteration'
      field-name: 'Iteration'
      field-value: '@current'
```
<!--/usage-->
