# <!--name-->slack/send<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Fslack%2Fsend+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)
[![test-slack-send](https://github.com/elastic/oblt-actions/actions/workflows/test-slack-send.yml/badge.svg?branch=main)](https://github.com/elastic/oblt-actions/actions/workflows/test-slack-send.yml)

## Inputs
<!--inputs-->
| Name               | Description                                                                                                                                                                                                                                                                                                                                                           | Required | Default |
|--------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|---------|
| `bot-token`        | Specify the slack bot token.                                                                                                                                                                                                                                                                                                                                          | `true`   | ` `     |
| `channel-id`       |                                                                                                                                                                                                                                                                                                                                                                       | `true`   | ` `     |
| `message`          | Slack message on Markdown format. Multiline messages must be escaped using URL encoding.<br>https://github.com/orgs/community/discussions/26288<br><br>This is an example how to escape a multiline message in Python:<br><pre>from urllib.parse import quote<br><br>message = quote("""<br>Hello!!!<br>This is a multiline message<br>""") # Multiline message</pre> | `true`   | ` `     |
| `thread-timestamp` | If you want to post a message as a threaded reply                                                                                                                                                                                                                                                                                                                     | `false`  | ` `     |
<!--/inputs-->

## Usage

<!--usage action="elastic/oblt-actions/**" version="env:VERSION"-->
```yaml
name: slack

jobs:
  slack:
    runs-on: ubuntu-latest
    steps:
      - uses: elastic/oblt-actions/slack/send@v1
        id: slack
        with:
          bot-token: ${{ secrets.SLACK_BOT_TOKEN }}
          channel-id: "#my-channel"
          message: "Run something"
      - uses: elastic/oblt-actions/slack/send@v1
        with:
          bot-token: ${{ secrets.SLACK_BOT_TOKEN }}
          channel-id: "#my-channel"
          message: "Run soemthing else"
          thread-timestamp: ${{ steps.slack.outputs.thread-timestamp || '' }}
```
<!--/usage-->
