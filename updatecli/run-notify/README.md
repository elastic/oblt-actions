# Updatecli run with slack notifications Github Action

* [Usage](#usage)
  * [Workflow](#workflow)
* [License](#license)

## Usage

Run Updatecli with Slack notifications for GitHub Action

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
        uses: elastic/oblt-actions/updatecli/run-notify@v2
        with:
          command: apply --config updatecli/updatecli.d
          slack-channel-id: "#my-channel"
          slack-message: "Run something"
          slack-bot-token: ${{ secrets.SLACK_BOT_TOKEN }}

```

**WARNING**: Don't enable --debug mode in Github Action as it may leak information.
