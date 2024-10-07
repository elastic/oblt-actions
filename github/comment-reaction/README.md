# <!--name-->github/comment-reaction<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Fgithub%2Fcomment-reaction+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)
[![test-github-comment-reaction](https://github.com/elastic/oblt-actions/actions/workflows/test-github-comment-reaction.yml/badge.svg?branch=main)](https://github.com/elastic/oblt-actions/actions/workflows/test-github-comment-reaction.yml)

<!--description-->
React to the given comment with an emoji (default +1).
<!--/description-->

## Inputs
<!--inputs-->
| Name           | Description                                                                                            | Required | Default                          |
|----------------|--------------------------------------------------------------------------------------------------------|----------|----------------------------------|
| `comment-id`   | The GitHub commentId                                                                                   | `false`  | `${{ github.event.comment.id }}` |
| `emoji`        | The GitHub emoji (see https://docs.github.com/en/rest/reactions?apiVersion=2022-11-28#about-reactions) | `false`  | `+1`                             |
| `github-token` | The GitHub access token.                                                                               | `false`  | `${{ github.token }}`            |
| `repository`   | The GitHub repository (format: ORG/REPO)                                                               | `false`  | `${{ github.repository }}`       |
<!--/inputs-->

## Usage

<!--usage action="elastic/oblt-actions/**" version="env:VERSION"-->
```yaml

on:
  issue_comment:
    types:
      - created
jobs:
  react:
    runs-on: ubuntu-latest
    if: ${{ github.event.issue.pull_request
    permission:
      issues: write
    steps:
      - uses: elastic/oblt-actions/github/comment-reaction@v1
        with:
          emoji: '-1'
      # ...
```
<!--/usage-->
