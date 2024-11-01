# <!--name-->github/is-pr-author-member-of<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Fgithub%2Fis-pr-author-member-of+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)

<!--description-->
Check whether the given GitHub Pull Request author is member of the given GitHub organization
<!--/description-->

## Inputs
<!--inputs-->
| Name           | Description                | Required | Default |
|----------------|----------------------------|----------|---------|
| `pull-request` | The GitHub Pull Request ID | `true`   | ` `     |
| `repository`   | The GitHub repository      | `true`   | ` `     |
| `github-org`   | The GitHub org             | `true`   | ` `     |
| `github-token` | The GitHub access token.   | `true`   | ` `     |
<!--/inputs-->

## Usage

<!--usage action="elastic/oblt-actions/**" version="env:VERSION"-->
```yaml
name: Is GitHub comment allowed
on:
  issues:
    types: [opened, edited]
jobs:
  run-action-if-pr-member-of-elastic-org:
    runs-on: ubuntu-latest
    steps:
      - uses: elastic/oblt-actions/github/is-pr-author-member-of@v1
        id: is_elastic_pr_author
        with:
          pull-request: ${{ steps.issue-parser.outputs.issueparser_kibana_pullrequest }}
          repository: "kibana"
          github-org: "elastic"
          github-token: ${{ secrets.PAT_TOKEN }}

      - if: steps.is_elastic_pr_author.outputs.result == true
        run: echo 'PR authr is member of'
      # ...
```
<!--/usage-->
