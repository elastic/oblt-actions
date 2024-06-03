# <!--name-->oblt-cli/cluster-name-validation<!--/name-->

<!--description-->
Get the cluster name based on the parameters
<!--/description-->

## Inputs
<!--inputs-->
| Name                | Description                           | Required | Default |
|---------------------|---------------------------------------|----------|---------|
| `cluster-name`      | The cluster name                      | `false`  | ` `     |
| `cluster-info-file` | The cluster info file (absolute path) | `false`  | ` `     |
<!--/inputs-->

## Outputs
<!--outputs-->
| Name           | Description      |
|----------------|------------------|
| `cluster-name` | The cluster name |
<!--/outputs-->

## Usage
<!--usage action="elastic/oblt-actions/oblt-cli/cluster-name-validation" version="env:VERSION"-->
```yaml
jobs:
  get-cluster-name:
    runs-on: ubuntu-latest
    steps:
      - id: cluster
        uses: elastic/oblt-actions/oblt-cli/cluster-name-validation@v1
        with:
          cluster-name: 'edge-oblt'
      - run: echo "${{ steps.cluster.outputs.cluster-name }}
```

or alternatively if you use `oblt-cli` with `--output-file "${CLUSTER_INFO_FILE}"'` then

```yaml
jobs:
  job:
    runs-on: ubuntu-latest
    steps:
      - uses: elastic/oblt-actions/oblt-cli/setup@v1
      - run: oblt-cli cluster create ... --output-file "${{ github.workspace }}/cluster-info.json" --wait 15
      - id: cluster
        uses: elastic/oblt-actions/oblt-cli/cluster-name-validation@v1
        with:
          cluster-info-file: ${{ github.workspace }}/cluster-info.json
      - run: echo "${{ steps.cluster.outputs.cluster-name }}
```
<!--/usage-->
