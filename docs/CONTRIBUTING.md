# Contribution Guidelines

## Prerequisites

### Pre-commit

This repository uses [pre-commit](https://pre-commit.com/) to enforce code quality.
To install pre-commit follow the instructions [here](https://pre-commit.com/#install).

After installing pre-commit, run the following command to install the pre-commit hooks:

```bash
pre-commit install
```

## Action Naming

This repository supports two action layout patterns:

- single-segment actions, for example: `feature-freeze`, `pre-commit`, `test-report`
- namespaced actions, for example: `updatecli/run`, `slack/send`

Example usage for a namespaced action:

```yaml
steps:
  - uses: elastic/oblt-actions/updatecli/run@v1
```

Example usage for a single-segment action:

```yaml
steps:
  - uses: elastic/oblt-actions/feature-freeze@v1
```

The directory structure can therefore include both styles:

```
oblt-actions/
├── feature-freeze/
│   └── action.yml
├── updatecli/
│   └── run/
│       └── action.yml
├── slack/
│   ├── send/
│   │   └── action.yml
│   └── notify-result/
│       └── action.yml
├── ...
├── ...
└── ...
```

## Action Testing

Every action should have a test workflow in the `.github/workflows` directory.
If the action name is `my/new-action`, then the test workflow should be named `test-my-new-action.yml.`

The workflow must have a job named `test` because the `test` status check is a required check for the `main` branch.

If you need to multiple jobs in the workflow you can create a job named `test` which utilizes the [check-dependent-jobs](../check-dependent-jobs) action
to create a status check that is computed based on the status of the other jobs.

```yaml
name: test-<my-action>

on:
  merge_group: ~
  workflow_dispatch: ~
  push:
    paths:
      - '.github/workflows/test-<my-action>.yml'
      - '<action-path>/**'

permissions:
  contents: read

jobs:
  test:
    if: always()
    needs:
      - test-default
      - test-with-arg
    runs-on: ubuntu-latest
    steps:
      - id: check
        uses: elastic/oblt-actions/check-dependent-jobs@v1
        with:
          jobs: ${{ toJSON(needs) }}
      - run: ${{ steps.check.outputs.is-success }}

  test-default:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ./<action-path>

  test-with-arg:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - id: my-action
        uses: ./<action-path>
        with:
          arg: true

      - name: Assert is oblt-hello-world
        run: test "${{ steps.my-action.outputs.pipeline }}" = "oblt-hello-world"
```

**NOTE**: replace `<my-action>` with the action name without `/` and `<action-path>` with the path to the action directory.

### .github/workflows/no-test.yml

Add `!<action-path>/**` in the `paths` section at `.github/workflows/no-test.yml`

**NOTE**: replace `<action-path>` with the path to the action directory.

## Pull request labels

Pull requests are validated by `.github/workflows/required-labels.yml`.
This check requires exactly one label from the release-drafter label set (including excluded labels) defined in `.github/release-drafter.yml`.

If the `required-labels` check fails:
- ensure one and only one release-drafter category label is applied to the PR
- remove extra release labels so only a single matching label remains
- if no matching label exists yet, add the appropriate release label for your change type

## Action Documentation
Every action should have a `README.md` file in its directory.
The `README.md` file is generated and updated with the `action-readme`
pre-commit hook provided by [gh-action-readme](https://github.com/reakaleek/gh-action-readme).

If you are adding a new action, you can use the following template to create the `README.md` file
and replace `<action-path>` with the path to the action directory or remove sections that are not applicable:

````markdown
# <!--name--><!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2F<action-path>+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)
[![test-<action-path>](https://github.com/elastic/oblt-actions/actions/workflows/test-<action-path>.yml/badge.svg?branch=main)](https://github.com/elastic/oblt-actions/actions/workflows/test-<action-path>.yml)

<!--description-->
<!--/description-->

## Inputs

<!--inputs-->
<!--/inputs-->

## Outputs

<!--outputs-->
<!--/outputs-->

## Usage
<!--usage action="elastic/oblt-actions/<action-path>" version="env:VERSION"-->
```yaml
steps:
  - uses: elastic/oblt-actions/<action-path>@v1
```
<!--/usage-->
````

Then run the following command to update the `README.md` file:

```bash
VERSION=v1 gh action-readme update
```
