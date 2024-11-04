# <!--name-->kibana-docker-image<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Fkibana-docker-image+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)
[![test-kibana-docker-image](https://github.com/elastic/oblt-actions/actions/workflows/test-kibana-docker-image.yml/badge.svg?branch=main)](https://github.com/elastic/oblt-actions/actions/workflows/test-kibana-docker-image.yml)

<!--description-->
An Action to build and push Kibana docker images given a git ref.
<!--/description-->

## Inputs

<!--inputs-->
| Name                | Description                                                                      | Required | Default                |
|---------------------|----------------------------------------------------------------------------------|----------|------------------------|
| `github-repository` | The git repository to build the image from.                                      | `false`  | `elastic/kibana`       |
| `git-ref`           | The git ref of elastic/kibana to build the image from. (Default: default branch) | `false`  | ` `                    |
| `serverless`        | Whether to build the serverless image or not.                                    | `false`  | `false`                |
| `docker-registry`   | Docker registry to publish the image to.                                         | `false`  | `docker.elastic.co`    |
| `docker-namespace`  | Docker namespace to publish the image to.                                        | `false`  | `observability-ci`     |
| `checkout-path`     | The path to checkout the git repository to.                                      | `false`  | `kibana-repo-checkout` |
<!--/inputs-->

## Outputs

<!--outputs-->
| Name                   | Description                                                               |
|------------------------|---------------------------------------------------------------------------|
| `kibana-docker-image`  | The reference of the Docker image that was built in the format image:tag. |
| `kibana-commit-sha`    | The git commit SHA of the image that was built.                           |
| `kibana-stack-version` | The elastic stack version of Kibana that was built.                       |
<!--/outputs-->

## Usage

<!--usage action="elastic/oblt-actions/**" version="env:VERSION"-->
```yaml
---
name: example

on: workflow_dispatch

jobs:
  kibana-docker-image-cloud:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Log in to the Elastic Container registry
        uses: docker/login-action@9780b0c442fbb1117ed29e0efdff1e18412f7567 # v3.3.0
        with:
          registry: ${{ secrets.ELASTIC_DOCKER_REGISTRY }}
          username: ${{ secrets.ELASTIC_DOCKER_USERNAME }}
          password: ${{ secrets.ELASTIC_DOCKER_PASSWORD }}

      - uses: 'elastic/oblt-actions/kibana-docker-image@v1'
        id: kibana-docker-image
        with:
          git-ref: main # git ref of elastic/kibana
          serverless: true # Default: false

      - name: docker pull
        run: |
          echo "${DOCKER_IMAGE:?}"
          docker pull "${DOCKER_IMAGE}"
        env:
          DOCKER_IMAGE: ${{ steps.kibana-docker-image.outputs.kibana-docker-image }}
```
<!--/usage-->
