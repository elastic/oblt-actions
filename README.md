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
- pull request events (`opened`, `synchronize`, `reopened`)
- pull request review submissions (`submitted`)

This workflow requires the repository secret `COPILOT_GITHUB_TOKEN`.

## Releasing

See [RELEASE.md](docs/RELEASE.md) for the release process.

<sup><br>Made with ♥️ and ☕️ by Elastic and our community.</sup>
