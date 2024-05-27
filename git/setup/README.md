# git/setup

GitHub Action that setups the git username, email, and authentication with git CLI

## Inputs

| name           | description             | required | default                                |
|----------------|-------------------------|----------|----------------------------------------|
| `username`     | <p>Git username</p>     | `false`  | `obltmachine`                          |
| `email`        | <p>Git email</p>        | `false`  | `obltmachine@users.noreply.github.com` |
| `trace`        | <p>Enable git trace</p> | `false`  | `false`                                |
| `github-token` | <p>GitHub token</p>     | `false`  | `${{ github.token }}`                  |

## Exported Environment Variables

| name       | description             |
|------------|-------------------------|
| `GIT_USER` | <p>Git username</p>     |
| `GIT_EMAIL`| <p>Git email</p>        |

## Usage

```yaml
---
name: deploy
on:
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      # ...
      - uses: elastic/oblt-actions/git/setup@v1
        with:
          username: "John"
          email: "john@acme.com"
          github-token: ${{ secrets.MY_GITHUB_PAT }}
      # ...
```
