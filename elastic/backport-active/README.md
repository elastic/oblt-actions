# Backport Action

A GitHub Action that automatically adds backport comments to merged pull requests based on labels.

## Usage

This action listens for merged pull requests with specific labels and adds a comment to trigger [Mergify](https://mergify.com/) backporting.

### Labels

The action recognizes the following labels:
- `backport-active-all`: Backport to all available branches
- `backport-active-8`: Backport to 8.x branches only
- `backport-active-9`: Backport to 9.x branches only

### Example Workflow

```yaml
name: Backport

on:
  pull_request:
    types: [closed]
    branches:
      - main

permissions:
  pull-requests: write
  issues: write
  contents: read

jobs:
  backport:
    if: github.event.pull_request.merged == true
    runs-on: ubuntu-latest
    steps:
      - uses: owner/backport-action@v1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          backports_url: "https://raw.githubusercontent.com/your-org/your-repo/main/config/branches.json"
```

### Configuration JSON Format

The action expects a JSON file containing the list of branches available for backporting:

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

## Inputs

| Name | Description | Required | Default |
|------|-------------|----------|---------|
| `github_token` | GitHub token for API access | Yes | `${{ github.token }}` |
| `backports_url` | URL to the JSON file with branch configurations | Yes | - |

## How it Works

1. When a PR is merged to the main branch, the action checks for backport labels
2. It fetches the branch configuration from the specified URL
3. Based on the labels, it filters which branches should receive the backport
4. It adds a comment with the format `@mergifyio backport branch1 branch2 ...` to trigger the backport process
