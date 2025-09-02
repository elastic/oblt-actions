#!/usr/bin/env python

import json
import os
import requests

class Inputs:
    def __init__(self):
        self.branches_to_exclude = os.environ.get('EXCLUDE_BRANCHES', '')
        self.filter_branches = os.environ.get('FILTER', 'false')
        self.repository = os.environ.get('REPOSITORY', '')
        self.github_token = os.environ.get('GITHUB_TOKEN', '')

class Outputs:
    def __init__(self):
        self.matrix = dict()
        self.branches = list()

class Env:
    def __init__(self):
        self.github_output = os.environ.get('GITHUB_OUTPUT')

def fails(msg: str) -> None:
    print(f'ERROR: {msg}')
    exit(1)

def get(url: str, headers: dict = None) -> requests.Response:
    response = requests.get(url, headers=headers if headers else {})
    response.raise_for_status()
    return response

def main(releases_url: str, github_url: str) -> Outputs:
    # Input and Output objects
    inputs = Inputs()
    outputs = Outputs()

    # Define vars
    active_branches = list()
    active_branches_after_exclusion = list()
    active_branches_after_filter = list()

    # Get active branches
    try:
        response = get(releases_url)
        payload = response.json()
        active_branches = [branch['branch'] for branch in payload['releases'] if branch['active_release'] == True]
    except requests.exceptions.HTTPError as e:
        fails(f'Failed to fetch releases. HTTP Error: {e}')
    except json.decoder.JSONDecodeError as e:
        fails(f'Failed to decode json response. JSON DecodeError: {e}')

    # Exclude branches
    if inputs.branches_to_exclude:
        branches_to_exclude = set(filter(lambda branch: len(branch) > 0, inputs.branches_to_exclude.split(',')))
        if branches_to_exclude:
            active_branches_after_exclusion = list(filter(lambda branch: branch not in branches_to_exclude, active_branches))
        active_branches = active_branches_after_exclusion

    # Filter branches
    should_be_filtered = inputs.filter_branches.lower() in ('true', '1', 't', 'y', 'yes')
    if inputs.repository and should_be_filtered:
        headers = {'Accept': 'application/vnd.github.v3+json'}
        if inputs.github_token:
            headers['Authorization'] = f'token {inputs.github_token}'
        for active_branch in active_branches:
            try:
                _ = get(f'{github_url}/repos/{inputs.repository}/branches/{active_branch}', headers=headers)
                active_branches_after_filter.append(active_branch)
            except requests.exceptions.HTTPError as e:
                fails(f'Branch {active_branch} does NOT exist in the repository {inputs.repository}. HTTP Error: {e}')
                continue
        active_branches = active_branches_after_filter

    include_branches = list(map(lambda branch: {"branch": branch}, active_branches))
    outputs.matrix = {'include': include_branches}
    outputs.branches = active_branches

    return outputs

if __name__ == "__main__":
    env = Env()
    future_releases_url = "https://artifacts.elastic.co/releases/TfEVhiaBGqR64ie0g0r0uUwNAbEQMu1Z/future-releases/stack.json"
    github_url = "https://api.github.com"
    outputs = main(
        releases_url=future_releases_url,
        github_url=github_url
    )

    with open(env.github_output, "a") as f:
        f.write(f"matrix={json.dumps(outputs.matrix)}\n")
        f.write(f"branches={json.dumps(outputs.branches)}\n")

    print(f"INFO: matrix={json.dumps(outputs.matrix)}")
    print(f"INFO: branches={json.dumps(outputs.branches)}")
