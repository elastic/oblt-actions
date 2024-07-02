# <!--name-->aws/auth<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Faws%2Fauth+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)
[![test-aws-auth](https://github.com/elastic/oblt-actions/actions/workflows/test-aws-auth.yml/badge.svg?branch=main)](https://github.com/elastic/oblt-actions/actions/workflows/test-aws-auth.yml)

<!--description-->
This is an opinionated GitHub Action to authenticate with AWS.

It generates a role ARN based on the repository name and the workflow filename, which is compatible with the
AWS role ARN we use for Elastic Observability repositories.
<!--/description-->

## Inputs
<!--inputs-->
| Name                    | Description                                                                                                                      | Required | Default        |
|-------------------------|----------------------------------------------------------------------------------------------------------------------------------|----------|----------------|
| `aws-account-id`        | The AWS account ID                                                                                                               | `false`  | `697149045717` |
| `aws-region`            | The AWS region, e.g. us-east-1                                                                                                   | `false`  | `us-east-1`    |
| `role-duration-seconds` | The assumed role duration in seconds, if assuming a role. Defaults to 1 hour, but cannot exceed the maximum defined by the role. | `false`  | `3600`         |
<!--/inputs-->

## Outputs
<!--outputs-->
| Name       | Description            |
|------------|------------------------|
| `role-arn` | The generated role ARN |
<!--/outputs-->

## Usage
<!--usage action="elastic/oblt-actions/**" version="env:VERSION"-->
```yaml
steps:
  - uses: elastic/oblt-actions/aws/auth@v1
    with:
      aws-region: 'us-east-1'
  - run: aws s3 ls
```
<!--/usage-->
