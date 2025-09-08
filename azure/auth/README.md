# <!--name-->azure-auth<!--/name-->
<!--description-->
Authenticate to Azure using a service principal with OIDC.
<!--/description-->
## Inputs
<!--inputs-->
| Name             | Description                                   | Required | Default |
|------------------|-----------------------------------------------|----------|---------|
| `subscriptionId` | The Azure subscription ID to authenticate to. | `true`   | ` `     |
| `tenantId`       | The Azure tenant ID.                          | `true`   | ` `     |
| `clientId`       | The Azure client ID (Service Principal).      | `true`   | ` `     |
<!--/inputs-->
## Outputs
<!--outputs-->
| Name | Description |
|------|-------------|
<!--/outputs-->
## Usage
<!--usage action="your/action" version="v1"-->
```yaml
on: push
steps:
  - uses: your/action@v1
```
<!--/usage-->
