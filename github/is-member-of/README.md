# <!--name-->github/is-member-of<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Fgithub%2Fis-member-of+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)

<!--description-->
Check whether the given GitHub user is a member of the given GitHub organization
<!--/description-->

## Inputs
<!--inputs-->
| Name           | Description              | Required | Default |
|----------------|--------------------------|----------|---------|
| `github-user`  | The GitHub user          | `true`   | ` `     |
| `github-org`   | The GitHub org           | `true`   | ` `     |
| `github-token` | The GitHub access token. | `true`   | ` `     |
| `exclude-bots` | Exclude bots             | `false`  | `true`  |
<!--/inputs-->

## Usage

<!--usage action="elastic/oblt-actions/**" version="env:VERSION"-->
```yaml
name: Is GitHub comment allowed
on:
  issue_comment:
    types: [created]
jobs:
  run-action-if-comment:
    runs-on: ubuntu-latest
    steps:
      - uses: elastic/oblt-actions/github/is-member-of@v1
        with:
          github-user: ${{ github.event.issue.user.login }}
          github-org: "elastic"
          github-token: ${{ secrets.PAT_TOKEN }}

      - if: steps.is_elastic_member.outputs.result == true
        run: echo '${{ github.event.issue.user.login }} is member'
      # ...
```
<!--/usage-->
