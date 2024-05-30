## About

Evaluates the combined the status results of the provided needs context.
This is useful for creating a single status check.

That status check can then be set as required status check, or it can be used
in combination with the `notify-built-status` action.

## Inputs

Following inputs can be used as `step.with` keys

| Name         | Type    | Default                     | Description                      |
|--------------|---------|-----------------------------|----------------------------------|
| `needs`      | String  |                             | JSON string of the needs context |

## Outputs

| Name         | Type    | Description                        |
|--------------|---------|------------------------------------|
| `is-success` | Boolean | If all jobs are successful or not. |
| `status`     | String  | `success` or `failure`             |


## Usage

```yaml
jobs:
  job-a:
    runs-on: ubuntu-latest
    steps:
      - run: exit 1;
  job-b:
    runs-on: ubuntu-latest
    steps:
      - run: exit 0;
  job-c:
    if: always()
    runs-on: ubuntu-latest
    needs:
      - job-a
      - job-b
    steps:
      - id: check
        uses: elastic/oblt-actions/check-dependent-jobs@v1
        with:
          needs: ${{ toJSON(needs) }}
      - run: ${{ steps.check.outputs.is-success }} # should exit with 1 or 0.
```
