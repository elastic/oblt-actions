# updatecli/run-and-notify

* [Inputs](#inputs)
* [Usage](#usage)
  * [Workflow](#workflow)

## Inputs

| name               | description                                               | required | default  |
|--------------------|-----------------------------------------------------------|----------|----------|
| `command`          | <p>The updatecli command to run</p>                       | `true`   |          |
| `slack-bot-token`  | <p>The slack bot token</p>                                | `true`   |          |
| `slack-channel-id` | <p>The slack channel ID</p>                               | `true`   |          |
| `slack-message`    | <p>The slack message to be sent in MD format</p>          | `true`   |          |
| `slack-send-when`  | <p>When to send the message (always, success, failure)</p>| `false`  | `always` |

## Usage

Run Updatecli with Slack notifications for GitHub Action

### Workflow

```yaml
jobs:
  updatecli:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: elastic/oblt-actions/updatecli/run-and-notify@v2
        with:
          command: apply --config updatecli/updatecli.d
          slack-bot-token: ${{ secrets.SLACK_BOT_TOKEN }}
          slack-channel-id: "#my-channel"
          slack-message: "Automation failed"
          slack-send-when: 'failure'
```
