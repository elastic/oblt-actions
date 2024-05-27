# git/setup

GitHub Action that setups the git username, email, and authentication with git CLI

## Inputs

| name           | description             | required | default                                |
|----------------|-------------------------|----------|----------------------------------------|
| `username`     | <p>Git username</p>     | `false`  | `obltmachine`                          |
| `email`        | <p>Git email</p>        | `false`  | `obltmachine@users.noreply.github.com` |
| `trace`        | <p>Enable git trace</p> | `false`  | `false`                                |
| `github-token` | <p>GitHub token</p>     | `false`  | `${{ github.token }}`                  |

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
