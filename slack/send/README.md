# slack/send Github Action

* [Usage](#usage)
  * [Workflow](#workflow)
* [License](#license)

## Usage

Send a slack message for GitHub Action

### Workflow

```yaml
name: slack

jobs:
  slack:
    runs-on: ubuntu-latest
    steps:
      - uses: elastic/oblt-actions/slack/send@v1
        with:
          channel-id: "#my-channel"
          message: "Run something"
          bot-token: ${{ secrets.SLACK_BOT_TOKEN }}
```
