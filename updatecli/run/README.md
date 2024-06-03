# <!--name-->updatecli/run<!--/name-->

## Inputs

<!--inputs-->
| Name      | Description                                   | Required | Default |
|-----------|-----------------------------------------------|----------|---------|
| `command` | Specify the updatecli command to be executed. | `true`   | ` `     |
<!--/inputs-->

## Usage

<!--usage action="elastic/oblt-actions/updatecli/run" version="env:VERSION"-->
```yaml
name: updatecli

jobs:
  updatecli:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Install Updatecli in the runner
        uses: elastic/oblt-actions/updatecli/run@v1
        with:
          command: apply --config updatecli/updatecli.d
```
<!--/usage-->
