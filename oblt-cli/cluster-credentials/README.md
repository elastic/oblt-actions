# oblt-cli/cluster-credentials

Run the oblt-cli wrapper to retrieve the credentials to connect to the given cluster.

## Inputs

| Name                    | Required | Description                                       | Default |
|-------------------------|----------|-------------------------------------------------- |---------|
| `cluster-name `         | `false`  | The cluster name                                  | -       |
| `cluster-info-file `    | `false`  | The cluster info file (absolute path)             | -       |
| `github-token`          | `true`   | The GitHub token with permissions fetch releases. | -       |

## Exported Environment Variables

Masked environment variables that are available:

* ELASTIC_APM_SERVER_URL
* ELASTIC_APM_JS_SERVER_URL
* ELASTIC_APM_JS_BASE_SERVER_URL
* ELASTIC_APM_SECRET_TOKEN
* ELASTIC_APM_API_KEY
* ELASTICSEARCH_API_TOKEN
* ELASTICSEARCH_HOSTS
* ELASTICSEARCH_HOST
* ELASTICSEARCH_USERNAME
* ELASTICSEARCH_PASSWORD
* FLEET_ELASTICSEARCH_HOST
* FLEET_ENROLLMENT_TOKEN
* FLEET_SERVER_SERVICE_TOKEN
* FLEET_SERVER_POLICY_ID
* FLEET_TOKEN_POLICY_NAME
* FLEET_URL
* KIBANA_HOST
* KIBANA_HOSTS
* KIBANA_FLEET_HOST
* KIBANA_USERNAME
* KIBANA_PASSWORD

## Usage

```yaml
jobs:
  cat-indices:
    runs-on: ubuntu-latest
    steps:
      - uses: elastic/oblt-actions/oblt-cli/cluster-credentials@v1
        with:
          cluster-name: 'edge-oblt'
          github-token: ${{ secrets.PAT_TOKEN }}
      - run: curl -X GET ${ELASTICSEARCH_HOST}/_cat/indices?v -u ${ELASTICSEARCH_USERNAME}:${ELASTICSEARCH_PASSWORD}
```
