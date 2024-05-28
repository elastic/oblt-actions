## About

GitHub Action to gather the cluster-name and run some validation based on the different inputs.
This is likely to be used within other GitHub actions.

## Inputs

| name                | description                           | required | Default |
|---------------------|---------------------------------------|----------|---------|
| `cluster-name`      | The cluster name                      | `false`  | -       |
| `cluster-info-file` | The cluster info file (absolute path) | `false`  | -       |

## Outputs

| Name           | Type    | Description      |
|----------------|---------|------------------|
| `cluster-name` | String  | The cluster name |

## Usage

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
