# <!--name-->slack/build-result<!--/name-->

## Inputs
<!--inputs-->
| Name         | Description                                       | Required | Default |
|--------------|---------------------------------------------------|----------|---------|
| `channel-id` |                                                   | `true`   | ` `     |
| `bot-token`  | Specify the slack bot token.                      | `true`   | ` `     |
| `message`    | Specify the message to be sent (markdown format). | `true`   | ` `     |
<!--/inputs-->

## Usage

<!--usage action="elastic/oblt-actions/slack/build-result" version="env:VERSION"-->
```yaml
name: slack

jobs:
  slack:
    runs-on: ubuntu-latest
    steps:
      - uses: elastic/oblt-actions/slack/buld-result@v1
        with:
          bot-token: ${{ secrets.SLACK_BOT_TOKEN }}
          channel-id: "#my-channel"
          message: "Run something"
```
<!--/usage-->
