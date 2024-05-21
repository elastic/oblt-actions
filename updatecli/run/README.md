# Updatecli run Github Action

* [Usage](#usage)
  * [Workflow](#workflow)
* [License](#license)

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
        uses: elastic/oblt-actions/updatecli/run@v2
        with:
          command: apply --config updatecli/updatecli.d

```

**WARNING**: Don't enable --debug mode in Github Action as it may leak information.
