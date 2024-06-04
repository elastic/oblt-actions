# Contribution Guidelines

## Prerequisites

### Pre-commit

This repository uses [pre-commit](https://pre-commit.com/) to enforce code quality.
To install pre-commit follow the instructions [here](https://pre-commit.com/#install).

After installing pre-commit, run the following command to install the pre-commit hooks:

```bash
pre-commit install
```

### GitHub CLI

This repository uses the [gh-action-readme](https://github.com/reakaleek/gh-action-readme) GitHub CLI extension to generate and update the `README.md` files for the actions.
To install the GitHub CLI follow the instructions [here](https://github.com/cli/cli#installation).

After installing the GitHub CLI, run the following command to install the `gh-action-readme` extension:

```bash
gh extension install reakaleek/gh-action-readme
```

## Action Documentation
Every action should have a `README.md` file in its directory.
The `README.md` file is generated and updated by the [gh-action-readme](https://github.com/reakaleek/gh-action-readme)
GitHub CLI extension.

If you are adding a new action, you can use the following template to create the `README.md` file
and replace `<action-path>` with the path to the action directory.

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
