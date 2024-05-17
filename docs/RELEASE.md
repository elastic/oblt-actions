# Release Process

This document outlines the process for releasing a new version of this project.

## Versioning

This project uses [Semantic Versioning](https://semver.org/) and its version is
automatically determined by [release-drafter](https://github.com/release-drafter/release-drafter)
based on the labels of the pull requests merged into the `main` branch.

See the [release-drafter configuration](.github/release-drafter.yml) for more details.

## Creating a New Release

Every time a pull request is merged into the `main` branch, release-drafter will
create or update a draft release in the [Releases](https://github.com/elastic/oblt-actions/releases) page.

To create a new release you need to publish the existing draft release created by release-drafter.

> [!NOTE]
> When a release is published, the [create-major-tag workflow](.github/workflows/create-major-tag.yml)
> will force push a new major tag in the format `vX` where `X` is the major version of the release.
> For example, if the release is `v1.2.3` was published, the workflow will force push a new tag `v1` on the same commit.
