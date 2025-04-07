# <!--name-->github/project-field-set<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Fgithub%2Fproject-field-set+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)
[![test-github-project-field-set](https://github.com/elastic/oblt-actions/actions/workflows/test-github-project-field-set.yml/badge.svg?branch=main)](https://github.com/elastic/oblt-actions/actions/workflows/test-github-project-field-set.yml)

<!--description-->
Sets field of an GitHub project item
<!--/description-->

## Inputs
<!--inputs-->
| Name              | Description                                                              | Required | Default               |
|-------------------|--------------------------------------------------------------------------|----------|-----------------------|
| `github-token`    | The GitHub access token.                                                 | `true`   | `${{ github.token }}` |
| `project-id`      | ID of the project                                                        | `true`   | ` `                   |
| `item-id`         | ID of item in the project                                                | `true`   | ` `                   |
| `field-name`      | Field name                                                               | `true`   | ` `                   |
| `field-value`     | Field value, when "field-iteration" = true the current iteration is used | `false`  | ` `                   |
| `field-iteration` | Must be set to "true" for iteration fields                               | `false`  | `false`               |
<!--/inputs-->

## Usage
<!--usage action="elastic/oblt-actions/github/project-field-set" version="env:VERSION"-->
```yaml
steps:
  - uses: elastic/oblt-actions/github/project-field-set@v1
```
<!--/usage-->
