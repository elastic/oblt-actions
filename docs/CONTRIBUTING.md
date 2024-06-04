# Contribution Guidelines

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
