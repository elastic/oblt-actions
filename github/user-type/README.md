# <!--name-->github/user-type<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Fgithub%2Fuser-type+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)
[![test-github-user-type](https://github.com/elastic/oblt-actions/actions/workflows/test-github-user-type.yml/badge.svg?branch=main)](https://github.com/elastic/oblt-actions/actions/workflows/test-github-user-type.yml)

<!--description-->
Get GitHub user type
<!--/description-->

## Inputs

<!--inputs-->
| Name           | Description              | Required | Default               |
|----------------|--------------------------|----------|-----------------------|
| `github-token` | The GitHub access token. | `true`   | `${{ github.token }}` |
| `github-user`  | The GitHub username      | `true`   | ` `                   |
<!--/inputs-->

## Outputs

<!--outputs-->
| Name     | Description                                                    |
|----------|----------------------------------------------------------------|
| `result` | The GitHub user type: `user` for regular users, `bot` for bots |
<!--/outputs-->

## Usage
<!--usage action="elastic/oblt-actions/github/user-type" version="env:VERSION"-->
```yaml
steps:
  steps:
    - uses: elastic/oblt-actions/github/user-type@v1
      with:
        github-token: <GITHUB_TOKEN>
        github-user: octocat
```
<!--/usage-->
