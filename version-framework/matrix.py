import json
import os
import yaml
from pathlib import Path


def run() -> None:
    excluded_file = os.getenv("EXCLUDED_FILE", "")
    framework_file = os.environ["FRAMEWORKS_FILE"]
    versions_file = os.environ["VERSIONS_FILE"]

    excludes = {'exclude': []}

    if len(excluded_file) > 0:
        excludes = yaml.safe_load(Path(excluded_file).read_text())
    frameworks = yaml.safe_load(Path(framework_file).read_text())
    versions = yaml.safe_load(Path(versions_file).read_text())

    matrix = {'include': []}
    for version in versions['VERSION']:
        for framework in frameworks['FRAMEWORK']:
            if len(list(filter(lambda item: item['VERSION'] == version and item["FRAMEWORK"] == framework, excludes['exclude']))) > 0:
                print('excluded ' + version + ' with ' + framework)
            else:
                matrix['include'].append({"version": version, "framework": framework})

    with open(os.environ.get('GITHUB_OUTPUT'), "a") as f:
        f.write("matrix={}\n".format(json.dumps(matrix)))

run()
