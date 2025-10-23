# <!--name-->download-kibana-dashboard<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Fdownload-kibana-dashboard+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)
[![test-download-kibana-dashboard](https://github.com/elastic/oblt-actions/actions/workflows/test-download-kibana-dashboard.yml/badge.svg?branch=main)](https://github.com/elastic/oblt-actions/actions/workflows/test-download-kibana-dashboard.yml)

<!--description-->
An Action to download a Kibana dashboard in png.
<!--/description-->

## Inputs

<!--inputs-->
| Name                | Description                                                                                           | Required | Default                |
|---------------------|-------------------------------------------------------------------------------------------------------|----------|------------------------|
| `kibana-host`       | The Kibana host URL.                                                                                  | `true`   | ` `                    |
| `kibana-user`       | The user reference for Kibana.                                                                        | `true`   | ` `                    |
| `kibana-password`   | The password for the Kibana user.                                                                     | `true`   | ` `                    |
| `dashboard-title`   | The title of the dashboard to generate the PNG for.                                                   | `false`  | `kibana-dashboard`     |
| `dashboard-id`      | The ID of the dashboard to generate the PNG for.                                                      | `true`   | ` `                    |
| `from-date`         | The start date for the report.                                                                        | `false`  | `now-15m`              |
| `to-date`           | The end date for the report.                                                                          | `false`  | `now`                  |
| `png-filename`      | The output file path for the generated PNG.                                                           | `false`  | `kibana-dashboard.png` |
| `table-width`       | The width of the table in pixels.                                                                     | `false`  | `2400`                 |
| `if-no-files-found` | The behavior when no files are found to upload. Options are 'error', 'warn', or 'ignore'.             | `false`  | `error`                |
| `max-retries`       | The maximum number of retries for fetching the dashboard with a pause of 10 seconds between attempts. | `false`  | `20`                   |
<!--/inputs-->

## Outputs

<!--outputs-->
| Name | Description |
|------|-------------|
<!--/outputs-->

## Usage

<!--usage action="elastic/oblt-actions/**" version="env:VERSION"-->
```yaml
---
  - uses: 'elastic/oblt-actions/download-kibana-dashboard@v1'
    with:
      kibana-host: "https://my-kibana.kb.us-central1.gcp.cloud.es.io:443"
      kibana-user: "my-kibana-user"
      kibana-password: ${{ secrets.MY_KIBANA_PASS }}
      dashboard-id: "my-dashboard-id"
      from-date: "2025-10-22T13:33:33.000Z"
      to-date: "2025-10-24T13:33:33.000Z"
```
<!--/usage-->
