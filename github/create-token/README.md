# <!--name-->github/create-token<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Fgithub%2Fcreate-token+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)
[![test-github-user-type](https://github.com/elastic/oblt-actions/actions/workflows/test-github-user-type.yml/badge.svg?branch=main)](https://github.com/elastic/oblt-actions/actions/workflows/test-github-user-type.yml)

<!--description-->
Create ephemeral GitHub token
<!--/description-->

## Inputs

<!--inputs-->
| Name                | Description                                                                          | Required | Default   |
|---------------------|--------------------------------------------------------------------------------------|----------|-----------|
| `vault-instance`    | The Vault instance to use for GitHub token retrieval                                 | `false`  | `ci-prod` |
| `token-policy`      | Vault role to assume for GitHub token retrieval if using wildcards in the subclaims. | `false`  | ` `       |
| `skip-token-revoke` | If true, skip revoking the GitHub token on exit                                      | `false`  | `false`   |
<!--/inputs-->

## Outputs

<!--outputs-->
| Name    | Description                |
|---------|----------------------------|
| `token` | The GitHub ephemeral token |
<!--/outputs-->

## Usage
<!--usage action="elastic/oblt-actions/github/create-token" version="env:VERSION"-->
```yaml
my-job:
  permissions:
    id-token: write
  steps:
    - uses: elastic/oblt-actions/github/create-token@v1
      id: fetch-token

    - uses: ...
      with:
        github-token: ${{ steps.fetch-token.outputs.token }}
```
<!--/usage-->
