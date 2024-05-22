# updatecli/install

* [Usage](#usage)
  * [Workflow](#workflow)

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
        uses: elastic/oblt-actions/updatecli/install@v1
```
