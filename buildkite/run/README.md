# buildkite/run

GitHub Action to run the buildkite

## Inputs


### inputs

Following inputs can be used as `step.with` keys

| Name         | Type    | Default                                             | Description                                                                                                       |
|--------------|---------|-----------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| `org`        | String  | `elastic`                                           | The Buildkite org.                                                                                                |
| `pipeline`   | String  |                                                     | The Buildkite pipeline to interact with.                                                                          |
| `branch`     | String  | `main`                                              | Branch the commit belongs to. This allows you to take advantage of your pipeline and step-level branch filtering rules. |
| `commit`     | String  | `HEAD`                                              | Ref, SHA or tag to be built.                                                                                      |
| `message`    | String  | `"Triggered automatically - ${{ github.workflow_ref }} (${{ github.event_name }})"`| The Buildkite build message to be shown in the UI.  |
| `token`      | String |                                             | The Buildkite API Token.                                                                          |
| `wait-for`   | boolean | `false`                                             | Whether to wait for the build to finish.                                                                          |
| `env-vars`   | String  |                                                     | Additional environment variables to set on the build, in KEY=VALUE format. No double quoting or extra `=`         |

### outputs

| Name              | Type    | Description                   |
|-------------------|---------| ------------------------------|
| `build`           | String  |  The Buildkite web Build URL. |
| `number`          | String  |  The Buildkite build number.  |
| `pipeline`        | String  |  The Buildkite pipeline. |
| `state`           | String  |  The Buildkite build state if `wait-for=true`. |
| `url`             | String  |  The Buildkite build URL.     |


## Usage

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
