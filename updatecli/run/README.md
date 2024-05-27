# updatecli/run

* [Inputs](#inputs)
* [Usage](#usage)
  * [Workflow](#workflow)

## Inputs

| name               | description                                               | required | default  |
|--------------------|-----------------------------------------------------------|----------|----------|
| `command`          | <p>The updatecli command to run</p>                       | `true`   |          |

## Usage

Install Updatecli for GitHub Action

### Workflow

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
