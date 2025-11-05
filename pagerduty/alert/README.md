# <!--name-->pagerduty-alert<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2F.github%2Factions%2Fpagerduty%2Falert+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)
[![test-pagerduty-alert](https://github.com/elastic/oblt-actions/actions/workflows/test-pagerduty-alert.yml/badge.svg?branch=main)](https://github.com/elastic/oblt-actions/actions/workflows/test-pagerduty-alert.yml)

<!--description-->
Raise a PagerDuty
<!--/description-->

## Inputs
<!--inputs-->
| Name          | Description                        | Required | Default    |
|---------------|------------------------------------|----------|------------|
| `summary`     | The PagerDuty summary of the alert | `true`   | ` `        |
| `source`      | The PagerDuty source of the alert  | `true`   | ` `        |
| `api-key`     | The PagerDuty API key              | `true`   | ` `        |
| `component`   | The PagerDuty component            | `true`   | ` `        |
| `routing-key` | The PagerDuty integration key      | `true`   | ` `        |
| `severity`    | The PagerDuty severity             | `false`  | `critical` |
<!--/inputs-->

## Outputs

<!--outputs-->
| Name           | Description                            |
|----------------|----------------------------------------|
| `incident-url` | The HTML URL of the PagerDuty incident |
<!--/outputs-->

## Usage
<!--usage action="elastic/oblt-actions/**" version="env:VERSION"-->
```yaml
jobs:
  assign-engineer-urgent-now:
    steps:
      - uses: elastic/oblt-actions/pagerduty/alert@v1
        id: pagerduty
        with:
          summary: "Reported some errors with XYZ"
          source: "https://..."
          api-key: "${{ secrets.PD_SECRET }}"
          component: "my-component"
          severity: "critical"
          routing-key: "abderg1231231312"

      - name: Notify a pagerduty incident has been created
        run: echo "${{steps.pagerduty.outputs.incident-url}} has been created"

```

<!--/usage-->
