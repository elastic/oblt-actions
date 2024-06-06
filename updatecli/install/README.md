# <!--name-->updatecli/install<!--/name-->

<!--description-->
This is an opinionated GitHub Action to install the updatecli
<!--/description-->

## Usage

<!--usage action="elastic/oblt-actions/**" version="env:VERSION"-->
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
<!--/usage-->
