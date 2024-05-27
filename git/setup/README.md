# git/setup

GitHub Action that setups the git username, email, and authentication with git CLI

## Inputs

| Name           | Type    | Default                                | Description        |
|----------------|---------|----------------------------------------|--------------------|
| `username`     | String  | `obltmachine`                          | Git username       |
| `secretId`     | String  | `obltmachine@users.noreply.github.com` | Git email.         |
| `trace`        | Boolean | `false`                                | Enable git trace.  |
| `token`        | String  | `github.token`                         | GitHub token.      |


## Usage

```yaml
---
name: deploy
on:
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      ...

      - uses: elastic/oblt-actions/git/setup@v1
        with:
          username: "John"
          email: "john@acme.com"
          token: ${{ secrets.MY_GITHUB_PAT }}
      ...
```
