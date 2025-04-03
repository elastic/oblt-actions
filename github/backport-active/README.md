# <!--name-->Backport Action<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Fgithub%2Fbackport-active+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)
[![test-github-backport-active](https://github.com/elastic/oblt-actions/actions/workflows/test-github-backport-active.yml/badge.svg?branch=main)](https://github.com/elastic/oblt-actions/actions/workflows/test-github-backport-active.yml)

<!--description-->
Automatically backport changes to specified branches based on PR labels
<!--/description-->

## Inputs
<!--inputs-->
| Name            | Description                                           | Required | Default                                                                |
|-----------------|-------------------------------------------------------|----------|------------------------------------------------------------------------|
| `github-token`  | GitHub token for authentication                       | `true`   | `${{ github.token }}`                                                  |
| `backports-url` | URL to fetch the backport branches configuration JSON | `true`   | `https://storage.googleapis.com/artifacts-api/snapshots/branches.json` |
| `dry-run`       | Run in dry-run mode without creating comments         | `true`   | `false`                                                                |
| `pr-number`     | PR number to use in dry-run mode                      | `true`   | `${{ github.event.pull_request.number }}`                              |
<!--/inputs-->

## Usage

Add this action to your workflow file:
<!--usage action="elastic/oblt-actions/**" version="env:VERSION"-->
```yaml
name: Backport

on:
  pull_request:
    types: [closed]
    branches:
      - main

permissions:
  pull-requests: write
  contents: read

jobs:
  backport:
    # Only run if the PR was merged (not just closed)
    if: github.event.pull_request.merged == true
    runs-on: ubuntu-latest
    steps:
      - uses: elastic/oblt-action/github/backport-action@v1
        with:
          backports-url: "https://storage.googleapis.com/artifacts-api/snapshots/branches.json"
```
<!--/usage-->

## Labels

The action recognizes the following labels:

- `backport-active-all`: Backport to all configured branches (except main)
- `backport-active-8`: Backport only to 8.x branches
- `backport-active-9`: Backport only to 9.x branches

You can also combine labels (e.g., having both `backport-active-8` and `backport-active-9`).

## Configuration JSON

The action requires a JSON configuration file with the available branches:

```json
{
  "branches": [
    "7.17",
    "8.x",
    "8.16",
    "8.17",
    "8.18",
    "9.0",
    "main"
  ]
}
```

## How It Works

1. When a PR is merged, the action checks for backport labels
2. It fetches the branch configuration from the specified URL
3. Based on the labels, it filters which branches should receive the backport
4. It adds a comment with the format `@mergifyio backport branch1 branch2 ...`
5. Mergify then handles the actual backporting process
