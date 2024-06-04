# <!--name-->slack/notify-result<!--/name-->

## Inputs
<!--inputs-->
| Name         | Description                                                                    | Required | Default |
|--------------|--------------------------------------------------------------------------------|----------|---------|
| `channel-id` |                                                                                | `true`   | ` `     |
| `bot-token`  | Specify the slack bot token.                                                   | `true`   | ` `     |
| `message`    | Add additional message to the notification.                                    | `false`  | ` `     |
| `status`     | Explicitly set status. One of success, failure, cancelled, auto. Default: auto | `false`  | `auto`  |
<!--/inputs-->

## Usage

<!--usage action="elastic/oblt-actions/slack/notify-result" version="env:VERSION"-->
```yaml
name: slack

jobs:
  slack:
    runs-on: ubuntu-latest
    steps:
      - uses: elastic/oblt-actions/slack/notify-result@v1
        with:
          bot-token: ${{ secrets.SLACK_BOT_TOKEN }}
          channel-id: "#my-channel"
          message: "Run something"
```
<!--/usage-->
