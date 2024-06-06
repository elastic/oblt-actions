# <!--name-->buildkite/run<!--/name-->

[![test-buildkite-run](https://github.com/elastic/oblt-actions/actions/workflows/test-buildkite-run.yml/badge.svg?branch=main)](https://github.com/elastic/oblt-actions/actions/workflows/test-buildkite-run.yml)

<!--description-->
A GitHub Action for triggering a build on a Buildkite pipeline.
<!--/description-->

## Inputs

<!--inputs-->
| Name       | Description                                                                                                             | Required | Default                                                                           |
|------------|-------------------------------------------------------------------------------------------------------------------------|----------|-----------------------------------------------------------------------------------|
| `branch`   | Branch the commit belongs to. This allows you to take advantage of your pipeline and step-level branch filtering rules. | `false`  | `main`                                                                            |
| `commit`   | Ref, SHA or tag to be built.                                                                                            | `false`  | `HEAD`                                                                            |
| `env-vars` | Additional environment variables to set on the build.                                                                   | `false`  | ` `                                                                               |
| `message`  | The BK build message to be shown in the UI.                                                                             | `false`  | `Triggered automatically - ${{ github.workflow_ref }} (${{ github.event_name }})` |
| `org`      | Buildkite org to interact with.                                                                                         | `false`  | `elastic`                                                                         |
| `pipeline` | Buildkite pipeline to interact with.                                                                                    | `true`   | ` `                                                                               |
| `token`    | Buildkite token.                                                                                                        | `true`   | ` `                                                                               |
| `wait-for` | Whether to wait for the build to finish.                                                                                | `false`  | `false`                                                                           |
<!--/inputs-->

## Outputs

<!--outputs-->
| Name       | Description                 |
|------------|-----------------------------|
| `build`    | The Buildkite web build url |
| `number`   | The Buildkite build number  |
| `pipeline` | The Buildkite pipeline      |
| `state`    | The Buildkite build state   |
| `url`      | The Buildkite build url     |
<!--/outputs-->

## Usage
<!--usage action="elastic/oblt-actions/**" version="env:VERSION"-->
```yaml
jobs:
  run-buildkite:
    runs-on: ubuntu-latest
    steps:
      - uses: elastic/oblt-actions/buildkite/run@v1
        with:
          token: ${{ secrets.BUILDKITE_TOKEN }}
          pipeline: 'my-super-pipeline'
```
<!--/usage-->
