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

Actions should be named using the following convention: `tool/action`.

For example, an action that runs updatecli should be named `updatecli/run`.

So that the usage of the action will be:

```yaml
steps:
  - uses: elastic/oblt-actions/updatecli/run@v1
```

Hence, the directory structure should look like this:

```
oblt-actions/
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
If the action name `my/new-action`, the test workflow should be named `test-my-new-action.yml`.

The workflow must have a job named `test` because the `test` status check is a required check for the `main` branch.

If you need to multiple jobs in the workflow you can create a job named `test` which utilizes the [check-dependent-jobs](../check-dependent-jobs) action
to create a status check that is computed based on the status of the other jobs.

## Action Documentation
Every action should have a `README.md` file in its directory.
The `README.md` file is generated and updated with the `action-readme`
pre-commit hook provided by [gh-action-readme](https://github.com/reakaleek/gh-action-readme).

If you are adding a new action, you can use the following template to create the `README.md` file
and replace `<action-path>` with the path to the action directory or remove sections that are not applicable:

````markdown
# <!--name--><!--/name-->
<!--description-->

## Inputs
<!--inputs-->

## Outputs
<!--outputs-->

## Usage
<--usage action="elastic/oblt-actions/<action-path>" version="env:VERSION"-->
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
