# <!--name-->github/validate-comment<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Fgithub%2Fvalidate-comment+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)

<!--description-->
Check whether the GitHub comment was triggered by a user with write permissions
<!--/description-->

## Inputs
<!--inputs-->
| Name | Description | Required | Default |
|------|-------------|----------|---------|
<!--/inputs-->

## Exported Environment Variables

| name       | description             |
|------------|-------------------------|
| `GIT_USER` | <p>Git username</p>     |
| `GIT_EMAIL`| <p>Git email</p>        |

## Usage

<!--usage action="elastic/oblt-actions/**" version="env:VERSION"-->
```yaml
---
name: Is GitHub comment allowed
on:
  issue_comment:
    types: [created]
jobs:
  run-action-if-comment:
    if: github.event.issue.pull_request && startsWith(github.event.comment.body, '/run-test')
    runs-on: ubuntu-latest
    steps:
      - uses: elastic/oblt-actions/github/validate-comment@v1
      # ...
```
<!--/usage-->
