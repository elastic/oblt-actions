# <!--name-->elastic/github-token<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Felastic%2Fgithub-token+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)
[![test-elastic-github-token](https://github.com/elastic/oblt-actions/actions/workflows/test-elastic-github-token.yml/badge.svg?branch=main)](https://github.com/elastic/oblt-actions/actions/workflows/test-elastic-github-token.yml)

<!--description-->
Fetch an ephemeral GitHub token from Vault using OIDC authentication
<!--/description-->

## Inputs
<!--inputs-->
| Name                | Description                           | Required | Default |
|---------------------|---------------------------------------|----------|---------|
| `skip-token-revoke` | Skip revoking the Vault token on exit | `false`  | `false` |
<!--/inputs-->

## Outputs

<!--outputs-->
| Name    | Description                           |
|---------|---------------------------------------|
| `token` | GitHub App installation access token. |
<!--/outputs-->

## Usage

<!--usage action="elastic/oblt-actions/**" version="env:VERSION"-->
```yaml
...
jobs:
  validate:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: elastic/oblt-actions/elastic/github-token@v1
        id: get_token

      - uses: ..
        with:
          github-token: ${{ steps.get_token.outputs.token }}

...
```
<!--/usage-->
