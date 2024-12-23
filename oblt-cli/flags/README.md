# <!--name-->oblt-cli/flags<!--/name-->
<!--description-->
Generate flags for oblt-cli.
<!--/description-->

## Inputs
<!--inputs-->
| Name                  | Description             | Required | Default |
|-----------------------|-------------------------|----------|---------|
| `cluster-name-prefix` | The cluster name prefix | `false`  | ` `     |
| `cluster-name-suffix` | The cluster name suffix | `false`  | ` `     |
| `dry-run`             | Whether to dryRun       | `false`  | `false` |
<!--/inputs-->

## Outputs
<!--outputs-->
| Name     | Description                        |
|----------|------------------------------------|
| `result` | The flags to be passed to oblt-cli |
<!--/outputs-->


## Usage
<!--usage action="elastic/oblt-actions/oblt-cli/flags" version="env:VERSION"-->
```yaml
steps:
  - uses: elastic/oblt-actions/oblt-cli/flags@v1
  - uses: elastic/oblt-actions/oblt-cli/lol@v1
```
<!--/usage-->
