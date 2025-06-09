# <!--name-->github/is-bot<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Fgithub%2Fis-bot+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)
[![test-github-is-bot](https://github.com/elastic/oblt-actions/actions/workflows/test-github-is-bot.yml/badge.svg?branch=main)](https://github.com/elastic/oblt-actions/actions/workflows/test-github-is-bot.yml)

<!--description-->
Tests if GitHub user is a bot or not
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
| Name     | Description                              |
|----------|------------------------------------------|
| `result` | `true` if user is bot, `false` otherwise |
<!--/outputs-->

## Usage
<!--usage action="elastic/oblt-actions/github/is-bot" version="env:VERSION"-->
```yaml
steps:
  steps:
    - uses: elastic/oblt-actions/github/is-bot@v1
      with:
        github-token: <GITHUB_TOKEN>
        github-user: octocat
```
<!--/usage-->
