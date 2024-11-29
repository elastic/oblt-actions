# <!--name-->updatecli/run-and-notify<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Fupdatecli%2Frun-and-notify+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)

> [!WARNING]
> *Deprecated* Will be removed in a future release.
> Please use the [updatecli/run](../run/README.md) action with the [slack/send](../../slack/send/README.md) action instead.

<!--description-->
This is an opinionated GitHub Action to run the updatecli with some slack
notifications.
<!--/description-->

## Inputs
<!--inputs-->
| Name               | Description                                         | Required | Default   |
|--------------------|-----------------------------------------------------|----------|-----------|
| `command`          | Specify the updatecli command to be executed.       | `true`   | ` `       |
| `slack-channel-id` |                                                     | `true`   | ` `       |
| `slack-bot-token`  | Specify the slack bot token.                        | `true`   | ` `       |
| `slack-message`    | Specify the message to be sent (markdown format).   | `true`   | ` `       |
| `slack-send-when`  | When to send the message, always, failure, success. | `false`  | `failure` |
<!--/inputs-->

## Usage
<!--usage action="elastic/oblt-actions/**" version="env:VERSION"-->
```yaml
jobs:
  updatecli:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: elastic/oblt-actions/updatecli/run-and-notify@v1
        with:
          command: apply --config updatecli/updatecli.d
          slack-bot-token: ${{ secrets.SLACK_BOT_TOKEN }}
          slack-channel-id: "#my-channel"
          slack-message: "Automation failed"
          slack-send-when: 'failure'
```
<!--/usage-->
