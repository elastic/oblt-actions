# <!--name-->check-dependent-jobs<!--/name-->

<!--description-->
Evaluates the combined the status results of the provided needs context.
<!--/description-->

## Inputs
<!--inputs-->
| Name   | Description                  | Required | Default |
|--------|------------------------------|----------|---------|
| `jobs` | needs context as JSON string | `true`   | ` `     |
<!--/inputs-->

## Outputs

<!--outputs-->
| Name         | Description                                                     |
|--------------|-----------------------------------------------------------------|
| `is-success` | The evaluated result of all provided jobs in the needs context. |
| `status`     | One of success or failure.                                      |
<!--/outputs-->

## Usage

<!--usage action="elastic/oblt-actions/check-dependent-jobs" version="env:VERSION"-->
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
          jobs: ${{ toJSON(needs) }}
      - run: ${{ steps.check.outputs.is-success }} # should exit with 1 or 0.
```
<!--/usage-->
