# <!--name-->git/setup<!--/name-->

<!--description-->
Setup the git usename, email, and authentication with git CLI.
After this action you can use https URL repos in git commands.
The GITHUB_TOKEN (not needed here) will be used to authenticate with the git CLI,
after this action.
<!--/description-->

## Inputs
<!--inputs-->
| Name           | Description      | Required | Default                                |
|----------------|------------------|----------|----------------------------------------|
| `username`     | Git username     | `false`  | `obltmachine`                          |
| `email`        | Git email        | `false`  | `obltmachine@users.noreply.github.com` |
| `trace`        | Enable git trace | `false`  | `false`                                |
| `github-token` | GitHub token     | `false`  | `${{ github.token }}`                  |
<!--/inputs-->

## Exported Environment Variables

| name       | description             |
|------------|-------------------------|
| `GIT_USER` | <p>Git username</p>     |
| `GIT_EMAIL`| <p>Git email</p>        |

## Usage

<!--usage action="elastic/oblt-actions/git/setup" version="env:VERSION"-->
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
<!--/usage-->
