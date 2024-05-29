# buildkite/run

GitHub Action to run the buildkite

## Inputs


### inputs

Following inputs can be used as `step.with` keys

| Name                        | Type    | Default                                             | Description                                                                                                       |
|-----------------------------|---------|-----------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| `org`                       | String  | `elastic`                                           | The Buildkite org.                                                                                                |
| `pipeline`                  | String  |                                                     | The Buildkite pipeline to interact with.                                                                          |
| `branch`            | String  | `main`                                              | Branch the commit belongs to. This allows you to take advantage of your pipeline and step-level branch filtering rules. |
| `commit`            | String  | `HEAD`                                              | Ref, SHA or tag to be built.                                                                                      |
| `message`            | String  | `Triggered automatically with GH actions`           | The Buildkite build message to be shown in the UI.                                                                |
| `wait-for`                   | boolean | `false`                                             | Whether to wait for the build to finish.                                                                          |
| `env-vars`              | String  |                                                     | Additional environment variables to set on the build, in KEY=VALUE format. No double quoting or extra `=`         |

### outputs

| Name              | Type    | Description               |
|-------------------|---------| --------------------------|
| `build`           | String  |  The Buildkite build URL. |
| `build_number`    | String  |  The Buildkite build URL. |
| `build_state`     | String  |  The Buildkite build URL. |


## Usage

```yaml
jobs:
  run-oblt-cli:
    runs-on: ubuntu-latest
    steps:
      - uses: elastic/oblt-actions/oblt-cli/run@v1
        with:
          command: 'cluster create ccs --remote-cluster=dev-oblt --cluster-name-prefix mycustomcluster'
          token: ${{ secrets.PAT_TOKEN }}
```
