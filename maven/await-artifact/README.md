# <!--name-->maven/await-artifact<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Fmaven%2Fawait-artifact+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)
[![test-maven-await-artifact](https://github.com/elastic/oblt-actions/actions/workflows/test-elastic-active-branches.yml/badge.svg?branch=main)](https://github.com/elastic/oblt-actions/actions/workflows/test-maven-await-artifact.yml)

<!--description-->
Waits for an artifact to be available on maven central
<!--/description-->

NOTE: this action does not timeout, hence you need to configure your GitHub workflow accordingly.
      See https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions#jobsjob_idstepstimeout-minutes

## Inputs
<!--inputs-->
| Name          | Description                         | Required | Default |
|---------------|-------------------------------------|----------|---------|
| `artifact-id` | Maven artifact-ID of the artifact   | `true`   | ` `     |
| `group-id`    | Maven group-ID of the artifact      | `true`   | ` `     |
| `version`     | Version of the artifact to wait for | `true`   | ` `     |
<!--/inputs-->


## Usage

<!--usage action="elastic/oblt-actions/**" version="env:VERSION"-->
```yaml
name: release
on:
  workflow_dispatch:
    inputs:
      version:
        description: 'The version to release (e.g. 1.2.3). This workflow will automatically perform the required version bumps'
        required: true
jobs:

  deploy:
    runs-on: ubuntu-latest
    steps:
      # ...
      - uses: elastic/oblt-actions/maven/await-artifact@v1
        timeout-minutes: 10
        with:
          group-id: "co.elastic.apm"
          artifact-id: "apm-agent-java"
          version: "${{ inputs.version }}"
      # ...
```
<!--/usage-->
