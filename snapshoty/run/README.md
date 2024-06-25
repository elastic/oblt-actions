# <!--name-->snapshoty/run<!--/name-->

[![usages](https://img.shields.io/badge/usages-white?logo=githubactions&logoColor=blue)](https://github.com/search?q=elastic%2Foblt-actions%2Fsnapshoty%2Frun+%28path%3A.github%2Fworkflows+OR+path%3A**%2Faction.yml+OR+path%3A**%2Faction.yaml%29&type=code)

<!--description-->
The best way to handle snapshot lifecycle.
<!--/description-->

## Inputs
<!--inputs-->
| Name                 | Description                                        | Required | Default |
|----------------------|----------------------------------------------------|----------|---------|
| `config`             | Path to configuration file                         | `true`   | ` `     |
| `bucket-name`        | Name of the bucket to use                          | `true`   | ` `     |
| `gcs-client-email`   | Google Cloud email of the service account          | `true`   | ` `     |
| `gcs-private-key`    | Google Cloud private key of the service account    | `true`   | ` `     |
| `gcs-private-key-id` | Google Cloud private key id of the service account | `true`   | ` `     |
| `gcs-project`        | Google Cloud project id of the service account     | `true`   | ` `     |
<!--/inputs-->

In addition, you can pass env variables with the prefix `SNAPSHOTY_`, the prefix will be removed and the name
of the variable will be passed.

## Usage

<!--usage action="elastic/oblt-actions/**" version="env:VERSION"-->
```yaml
    steps:
      - uses: elastic/oblt-actions/snapshoty/run@v1
        with:
          config: snapshoty.yml
          bucket-name: 'my-bucket'
          gcs-client-email: 'my-email@acme.org'
          gcs-private-ley: 'my-secret-key'
          gcs-private-key-id: 'my-private-key'
          gcs-project: 'my-gcs-project'
        env:
          SNAPSHOTY_DATE: "2023-09-20"
```

<!--/usage-->
