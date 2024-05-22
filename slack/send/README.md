# slack/send

* [Inputs](#inputs)
* [Usage](#usage)
  * [Workflow](#workflow)

## Inputs

| name         | description                                         | required | default  |
|--------------|-----------------------------------------------------|----------|----------|
| `bot-token`  | <p>The slack bot token</p>                          | `true`   |          |
| `channel-id` | <p>The slack channel ID</p>                         | `true`   |          |
| `message`    | <p>The slack message to be sent in MD format</p>    | `true`   |          |

## Usage

Send a Slack message for GitHub Action

### Workflow

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
