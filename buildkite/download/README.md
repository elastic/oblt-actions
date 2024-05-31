# buildkite/download

GitHub Action to download the artifacts for a given Buildkite build.

## Inputs

Following inputs can be used as `step.with` keys

| Name            | Type    | Default          | Description                                                          |
|-----------------|---------|----------------|------------------------------------------------------------------------|
| `artifact-path` | String  |                | A file, directory or wildcard pattern that describes what to download  |
| `build`         | String  |                | The Buildkite pipeline build.                                          |
| `org`           | String  | `elastic`      | The Buildkite org.                                                     |
| `pipeline`      | String  |                | The Buildkite pipeline to interact with.                               |
| `token`         | String  |                | The Buildkite API Token.                                               |

## Usage

```yaml
jobs:
  run-buildkite:
    runs-on: ubuntu-latest
    steps:
      - id: buildkite-run
        uses: elastic/oblt-actions/buildkite/run@v1
        with:
          token: ${{ secrets.BUILDKITE_TOKEN }}
          pipeline: "my-super-pipeline"
          wait-for: true

      - uses: elastic/oblt-actions/buildkite/download@v1
        with:
          artifact-path: "artifacts.tar"
          build: ${{ steps.buildkite-run.outputs.build }}
          pipeline: "my-super-pipeline"
          token: ${{ secrets.BUILDKITE_TOKEN }}
```
