import os
import json
import requests

def main():
    # Get environment variables
    github_token = os.environ['GITHUB_TOKEN']
    pr_number = int(os.environ['PR_NUMBER'])
    repository = os.environ['REPOSITORY']
    backports_url = os.environ['BACKPORTS_URL']
    print(f"Using backports URL: {backports_url}")

    # Define GitHub API headers
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    labels = []
    labels_json = os.environ.get('PR_LABELS', '[]')

    # If we have some JSON data, try to extract label names
    if labels_json and labels_json != 'null':
        try:
            labels_data = json.loads(labels_json)
            if isinstance(labels_data, list):
                for item in labels_data:
                    if isinstance(item, dict) and 'name' in item:
                        labels.append(item['name'])
        except json.JSONDecodeError:
            print(f"Invalid JSON in PR_LABELS: {labels_json}")

    # If no labels found, fetch from GitHub API (needed for non PR events)
    if not labels:
        try:
            url = f"https://api.github.com/repos/{repository}/issues/{pr_number}/labels"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                api_labels = response.json()
                for item in api_labels:
                    if isinstance(item, dict) and 'name' in item:
                        labels.append(item['name'])
            else:
                print(f"API returned status code: {response.status_code}")
        except Exception as e:
            print(f"Error fetching labels {str(e)}")

    print(f"Labels found: {labels}")

    # Function to get branches from URL (plain text, one branch per line)
    def get_branches_from_url(url):
        try:
            print(f"Fetching branches from URL: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return [line.strip() for line in response.text.splitlines() if line.strip()]
        except Exception as e:
            print(f"Error fetching branches from URL: {e}")
            return []

    # Always fetch from the backports URL
    target_branches = get_branches_from_url(backports_url)

    if target_branches:
        print(f"Found branches: {target_branches}")
    else:
        print("No branches found or config not available")

    # Filter branches based on the labels
    filtered_branches = []

    if 'backport-active-all' in labels:
        filtered_branches = [branch for branch in target_branches if branch != 'main' and branch != '7.17']
        print('Using all branches from JSON (excluding main) due to backport-active-all label')
    else:
        # Process 8.x and 9.x branches based on labels
        if 'backport-active-8' in labels:
            branches8 = [branch for branch in target_branches if
                        branch.startswith('8.') or branch == '8.x' or branch == '8']
            filtered_branches.extend(branches8)
            print(f"Found {len(branches8)} 8.x branches to backport")

        if 'backport-active-9' in labels:
            branches9 = [branch for branch in target_branches if
                        branch.startswith('9.') or branch == '9.x' or branch == '9']
            filtered_branches.extend(branches9)
            print(f"Found {len(branches9)} 9.x branches to backport")

    # Remove duplicates while preserving order
    seen = set()
    filtered_branches = [x for x in filtered_branches if not (x in seen or seen.add(x))]

    print(f"Final branches for backporting: {filtered_branches}")

    # Add comment to the PR if we have branches to backport to
    success = False
    if filtered_branches:
        comment = f"@mergifyio backport {' '.join(filtered_branches)}"

        # Create comment via GitHub API
        comment_url = f"https://api.github.com/repos/{repository}/issues/{pr_number}/comments"
        comment_data = {"body": comment}
        print(f'COMMENT_URL = {comment_url}')
        print(f'COMMENT_DATA = {comment_data}')

        print("Using GitHub token for authentication - comment will be posted")

        response = requests.post(comment_url, headers=headers, json=comment_data)

        if response.status_code == 201:
            print(f"Successfully added backport comment: {comment}")
            success = True
        else:
            print(f"Failed to add comment. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            success = False
    else:
        print("No branches to backport to after filtering")
        success = True  # No branches to backport is not an error condition

    return 0 if success else 1

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
