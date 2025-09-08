# <!--name-->azure-auth<!--/name-->
[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Fazure%2Fauth+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)
[![test-azure-auth](https://github.com/elastic/oblt-actions/actions/workflows/test-azure-auth.yml/badge.svg?branch=main)](https://github.com/elastic/oblt-actions/actions/workflows/test-azure-auth.yml)

<!--description-->
Authenticate to Azure using a service principal with OIDC.
<!--/description-->
## Inputs
<!--inputs-->
| Name              | Description                                   | Required | Default |
|-------------------|-----------------------------------------------|----------|---------|
| `subscription-id` | The Azure subscription ID to authenticate to. | `true`   | ` `     |
| `tenant-id`       | The Azure tenant ID.                          | `true`   | ` `     |
| `client-id`       | The Azure client ID (Service Principal).      | `true`   | ` `     |
<!--/inputs-->
## Outputs
<!--outputs-->
| Name | Description |
|------|-------------|
<!--/outputs-->
## Usage
<!--usage action="azure/auth" version="v1"-->
```yaml
jobs:
  job_id:
    permissions:
      id-token: write
    steps:
        - uses: elastic/oblt-actions/azure/auth@v1
          with:
            subscription-id: ${{ secrets.ARM_SUBSCRIPTION_ID }}
            tenant-id: ${{ secrets.ARM_TENANT_ID }}
            client-id: ${{ secrets.ARM_CLIENT_ID }}

        - run: az ...
```
<!--/usage-->
