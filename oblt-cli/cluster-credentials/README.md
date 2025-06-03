# <!--name-->oblt-cli/cluster-credentials<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Foblt-cli%2Fcluster-credentials+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)
[![test-oblt-cli-cluster-credentials](https://github.com/elastic/oblt-actions/actions/workflows/test-oblt-cli-cluster-credentials.yml/badge.svg?branch=main)](https://github.com/elastic/oblt-actions/actions/workflows/test-oblt-cli-cluster-credentials.yml)

<!--description-->
Run the oblt-cli wrapper to retrieve the credentials to connect to the given cluster
<!--/description-->

## Inputs
<!--inputs-->
| Name                | Description                           | Required | Default                 |
|---------------------|---------------------------------------|----------|-------------------------|
| `cluster-name`      | The cluster name                      | `false`  | ` `                     |
| `cluster-info-file` | The cluster info file (absolute path) | `false`  | ` `                     |
| `github-token`      | The GitHub access token.              | `true`   | ` `                     |
| `gcp-project-id`    | The GCP Project ID                    | `false`  | `elastic-observability` |
<!--/inputs-->

## Exported Environment Variables

Masked environment variables that are available:

* ELASTIC_AGENT_STANDALONE_API_KEY
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
* INGEST_URL
* KIBANA_HOST
* KIBANA_HOSTS
* KIBANA_FLEET_HOST
* KIBANA_FLEET_USERNAME
* KIBANA_FLEET_PASSWORD
* KIBANA_USERNAME
* KIBANA_PASSWORD
* SYNTHETICS_API_KEY

## Usage

<!--usage action="elastic/oblt-actions/**" version="env:VERSION"-->
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
<!--/usage-->
