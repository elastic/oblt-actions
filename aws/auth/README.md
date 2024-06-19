# <!--name-->aws/auth<!--/name-->
[![test-aws-auth](https://github.com/elastic/oblt-actions/actions/workflows/test-aws-auth.yml/badge.svg?branch=main)](https://github.com/elastic/oblt-actions/actions/workflows/test-aws-auth.yml)

<!--description-->
This is an opinionated GitHub Action to authenticate with AWS.

It generates a role ARN based on the repository name and the workflow filename, which is compatible with the
AWS role ARN we use for Elastic Observability repositories.
<!--/description-->

## Inputs
<!--inputs-->
| Name         | Description                    | Required | Default |
|--------------|--------------------------------|----------|---------|
| `aws-region` | The AWS region, e.g. us-east-1 | `true`   | ` `     |
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
