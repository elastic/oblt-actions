# GitHub Actions for Elastic Observability projects

[![GitHub release](https://img.shields.io/github/release/elastic/oblt-actions.svg?label=release&logo=github)](https://github.com/elastic/oblt-actions/releases/latest)

This repository contains GitHub Actions for Elastic Observability projects.

## Automation workflows

### Observability Agentic Workflow Entrypoint

The repository includes the `.github/workflows/oblt-aw.yml` workflow, which forwards selected repository events to the centralized `elastic/oblt-aw` ingress workflow.

It runs on:
- a daily schedule (`0 6 * * *`)
- manual dispatch (`workflow_dispatch`)
- issue events (`opened`, `labeled`)
- issue comment events (`created`)
- pull request events (`opened`, `synchronize`, `reopened`, `labeled`)

This workflow requires the repository secret `COPILOT_GITHUB_TOKEN`.

### updatecli automation

The repository includes the `.github/workflows/updatecli.yml` workflow, which runs Updatecli compose automation against `oblt-actions` and `observability-test-environments`.

It runs on:
- a weekly schedule (`0 6 * * 6`)
- manual dispatch (`workflow_dispatch`)

This workflow requires the repository secrets `OBS_AUTOMATION_APP_ID` and `OBS_AUTOMATION_APP_PEM` to generate a GitHub App token with write access to contents and pull requests for the target repositories.

## Releasing

See [RELEASE.md](docs/RELEASE.md) for the release process.

<sup><br>Made with ♥️ and ☕️ by Elastic and our community.</sup>
