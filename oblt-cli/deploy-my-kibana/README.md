# <!--name-->oblt-cli/deploy-my-kibana<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Foblt-cli%2Fdeploy-my-kibana+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)
[![test-oblt-cli-deploy-my-kibana](https://github.com/elastic/oblt-actions/actions/workflows/test-oblt-cli-deploy-my-kibana.yml/badge.svg?branch=main)](https://github.com/elastic/oblt-actions/actions/workflows/test-oblt-cli-deploy-my-kibana.yml)


<!--description-->
Run the deploy my Kibana PR.
<!--/description-->

## Inputs
<!--inputs-->
| Name                     | Description                                                 | Required | Default                                 |
|--------------------------|-------------------------------------------------------------|----------|-----------------------------------------|
| `comment-url`            | The GitHub Comment URL                                      | `false`  | `${{ github.event.comment.html_url }}`  |
| `comment-id`             | The GitHub Comment ID                                       | `false`  | `${{ github.event.comment.id }}`        |
| `issue-url`              | The GitHub Issue URL                                        | `false`  | `${{ github.event.comment.issue_url }}` |
| `repository`             | The GitHub repository                                       | `false`  | `${{ github.repository }}`              |
| `user`                   | The GitHub user that triggered the workflow                 | `false`  | `${{ github.triggering_actor }}`        |
| `github-token`           | The GitHub Personal Access Token.                           | `false`  | ` `                                     |
| `github-app-id`          | The GitHub App ID to generate the ephemeral token.          | `false`  | ` `                                     |
| `github-app-private-key` | The GitHub App Private Key to generate the ephemeral token. | `false`  | ` `                                     |
<!--/inputs-->

## Output
<!--outputs-->
| Name    | Description                                                   |
|---------|---------------------------------------------------------------|
| `issue` | The GitHub issue that has been created to destroy the cluster |
<!--/outputs-->

## Usage
<!--usage action="elastic/oblt-actions/**" version="env:VERSION"-->
```yaml
on:
  issue_comment:
    types: [created]
jobs:
  deploy-my-kibana:
    runs-on: ubuntu-latest
    permissions:
      # if you listen for PRs, use this to use some comment reactions
      pull-requests: write
      # if you listen for issues, use this to use some comment reactions
      issues: write
    steps:
      - uses: elastic/oblt-actions/oblt-cli/deploy-my-kibana@v1
        with:
          github-token: ${{ secrets.PAT_TOKEN }}
```
<!--/usage-->
