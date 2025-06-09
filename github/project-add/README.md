# <!--name-->github/project-add<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Fgithub%2Fproject-add+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)
[![test-github-project-add](https://github.com/elastic/oblt-actions/actions/workflows/test-github-project-add.yml/badge.svg?branch=main)](https://github.com/elastic/oblt-actions/actions/workflows/test-github-project-add.yml)

<!--description-->
Adds a GitHub issue or pull-request to a GitHub project
<!--/description-->

## Inputs

<!--inputs-->
| Name           | Description                              | Required | Default               |
|----------------|------------------------------------------|----------|-----------------------|
| `item-url`     | The GitHub issue/pull-request URL to add | `false`  | ` `                   |
| `github-org`   | The GitHub org                           | `true`   | `elastic`             |
| `github-token` | The GitHub access token.                 | `true`   | `${{ github.token }}` |
| `project-id`   | The GitHub project numeric ID.           | `true`   | ` `                   |
<!--/inputs-->

## Outputs

<!--outputs-->
| Name      | Description               |
|-----------|---------------------------|
| `item-id` | ID of item in the project |
<!--/outputs-->

## Usage
<!--usage action="elastic/oblt-actions/github/project-add" version="env:VERSION"-->
```yaml
steps:
  steps:
    - uses: elastic/oblt-actions/github/project-add@v1
      with:
        github-token: <GITHUB_TOKEN>
        github-org: elastic
        project-id: <PROJET_NUMERIC_ID>
        item-url: "https://github.com/elastic/apm-agent-java/pull/xxx"
```
<!--/usage-->
