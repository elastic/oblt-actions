#!/usr/bin/env python

import json
import os
import urllib.error
import urllib.request

def fails(msg):
    print(msg)
    exit(1)

try:
    with urllib.request.urlopen('https://elastic-release-api.s3.us-west-2.amazonaws.com/public/active-branches.txt') as response:
        branches = [line.strip() for line in response.read().decode('utf-8').splitlines() if line.strip()]
except Exception as e:
    fails(f"Failed to fetch active branches: {e}")

if not branches:
    fails("Failed to retrieve active branches")

exclude_branches = os.environ.get('EXCLUDE_BRANCHES', '')
exclude_branches = set(filter(lambda branch: len(branch) > 0, exclude_branches.split(',')))
if exclude_branches:
    branches = list(filter(lambda branch: branch not in exclude_branches, branches))

# Filter branches based on the existence in the GitHub repository
filter_str = os.environ.get('FILTER', 'false')
filter = filter_str.lower() in ('true', '1', 't', 'y', 'yes')
repository = os.environ.get('REPOSITORY', '')
if filter and repository:
    # Check if branches exist in the GitHub repository
    headers = {
        'Accept': 'application/vnd.github.v3+json'
    }
    github_token = os.environ.get('GITHUB_TOKEN', '')
    if github_token:
        headers['Authorization'] = f'token {github_token}'

    existing_branches = []
    for branch in branches:
        branch_url = f'https://api.github.com/repos/{repository}/branches/{branch}'
        request = urllib.request.Request(branch_url, headers=headers, method='GET')
        try:
            with urllib.request.urlopen(request) as response:
                if response.status == 200:
                    existing_branches.append(branch)
        except urllib.error.HTTPError as response:
            if response.code == 404:
                print(f"Not found (HTTP 404) when checking branch {branch} in repository {repository}. The branch or repository may not exist, or the token may lack access.")
            elif response.code == 401:
                print(f"Authentication failed for branch {branch} (HTTP 401). Check GITHUB_TOKEN.")
            elif response.code == 403:
                rate_limit_remaining = response.headers.get("X-RateLimit-Remaining")
                rate_limit_reset = response.headers.get("X-RateLimit-Reset")
                print(
                    f"Access forbidden for branch {branch} (HTTP 403)."
                    f"This may be due to rate limiting or missing permissions."
                )
                if rate_limit_remaining is not None or rate_limit_reset is not None:
                    print(
                        f"X-RateLimit-Remaining={rate_limit_remaining}, "
                        f"X-RateLimit-Reset={rate_limit_reset}"
                    )
            elif response.code >= 500:
                print(f"Server error while checking branch {branch} (HTTP {response.code}). GitHub API may be experiencing issues.")
            else:
                print(f"Unexpected error while checking branch {branch} (HTTP {response.code})")
        except urllib.error.URLError as response:
            print(f"Error while checking branch {branch}: {response}")

    branches = existing_branches

include_branches = list(map(lambda branch: {"branch": branch}, branches))
matrix = {'include': include_branches}

with open(os.environ.get('GITHUB_OUTPUT'), "a") as file_descriptor:
    file_descriptor.write(f"matrix={json.dumps(matrix)}\n")
    file_descriptor.write(f"branches={json.dumps(branches)}\n")

print(f"INFO: matrix={json.dumps(matrix)}")
print(f"INFO: branches={json.dumps(branches)}")
