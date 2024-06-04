# <!--name-->slack/send<!--/name-->

## Inputs
<!--inputs-->
| Name         | Description                                                                                                                                                                                                                                                                                                                                    | Required | Default |
|--------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|---------|
| `bot-token`  | Specify the slack bot token.                                                                                                                                                                                                                                                                                                                   | `true`   | ` `     |
| `channel-id` |                                                                                                                                                                                                                                                                                                                                                | `true`   | ` `     |
| `message`    | Slack message on Markdown format. Multiline messages must be escaped using URL encoding.
https://github.com/orgs/community/discussions/26288

This is an example how to escape a multiline message in Python:
```Python
from urllib.parse import quote

message = quote("""
Hello!!!
This is a multiline message
""") # Multiline message
```
 | `true`   | ` `     |
<!--/inputs-->

## Usage

<!--usage action="elastic/oblt-actions/slack/send" version="env:VERSION"-->
```yaml
name: slack

jobs:
  slack:
    runs-on: ubuntu-latest
    steps:
      - uses: elastic/oblt-actions/slack/send@v1
        with:
          bot-token: ${{ secrets.SLACK_BOT_TOKEN }}
          channel-id: "#my-channel"
          message: "Run something"
```
<!--/usage-->
