# <!--name-->test-report<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Ftest-report+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)

<!--description-->
Shows test results in GitHub UI: .NET (xUnit, NUnit, MSTest), Dart, Flutter, Java (JUnit), JavaScript (JEST, Mocha)
<!--/description-->

## Inputs

<!--inputs-->
| Name            | Description                                                                                                                                                                                                                                           | Required | Default       |
|-----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|---------------|
| `artifact`      | Name or regex of artifact containing test results                                                                                                                                                                                                     | `false`  | `all`         |
| `name`          | Name of the check run                                                                                                                                                                                                                                 | `false`  | `JUnit Tests` |
| `path`          | Coma separated list of paths to test results<br>Supports wildcards via [fast-glob](https://github.com/mrmlnc/fast-glob)<br>All matched result files must be of same format<br>                                                                        | `true`   | `**/*.xml`    |
| `reporter`      | Format of test results. Supported options:<br>  - dart-json<br>  - dotnet-trx<br>  - flutter-json<br>  - java-junit<br>  - jest-junit<br>  - mocha-json<br>  - mochawesome-json<br>                                                                   | `true`   | `java-junit`  |
| `list-suites`   | Limits which test suites are listed. Supported options:<br>  - all<br>  - failed<br>                                                                                                                                                                  | `true`   | `all`         |
| `list-tests`    | Limits which test cases are listed. Supported options:<br>  - all<br>  - failed<br>  - none<br>                                                                                                                                                       | `true`   | `all`         |
| `fail-on-error` | Set this action as failed if test report contain any failed test                                                                                                                                                                                      | `true`   | `true`        |
| `fail-on-empty` | Set this action as failed if no test results are found                                                                                                                                                                                                | `true`   | `false`       |
| `only-summary`  | Allows you to generate only the summary.<br>If enabled, the report will contain a table listing each test results file and the number of passed,<br>failed, and skipped tests.<br>Detailed listing of test suites and test cases will be skipped.<br> | `false`  | `false`       |
<!--/inputs-->

## Usage

<!--usage action="elastic/oblt-actions/**" version="env:VERSION"-->
```yaml
on:
  workflow_run:
    workflows:
      - test
    types:
      - completed

permissions:
  contents: read
  actions: read
  checks: write

jobs:
  report:
    runs-on: ubuntu-latest
    steps:
      - uses: elastic/oblt-actions/test-report@v1
        with:
          artifact: test-results
          name: JUnit Tests
          path: "**/*-python-agent-junit.xml"
          reporter: java-junit
```
<!--/usage-->
