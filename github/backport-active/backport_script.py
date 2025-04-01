import os
import json
import requests

def main():
    # Check if we're in test mode
    test_mode = os.environ.get('TEST_MODE', 'false').lower() == 'true'

    # Get environment variables
    github_token = os.environ['GITHUB_TOKEN']
    pr_number = int(os.environ['PR_NUMBER'])
    repo_owner = os.environ['REPO_OWNER']
    repo_name = os.environ['REPO_NAME']

    # Override GitHub API URL if set (for testing with mock server)
    github_api_url = os.environ.get('GITHUB_API_URL', 'https://api.github.com')

    # Get the backports URL from the environment variable
    backports_url = os.environ['BACKPORTS_URL']
    print(f"Using backports URL: {backports_url}")

    # Parse PR labels
    labels_json = os.environ['PR_LABELS']
    labels = [label['name'] for label in json.loads(labels_json)]
    print(f"PR Labels: {labels}")

    # Log if in test mode
    if test_mode:
        print("***** RUNNING IN TEST MODE *****")
        print(f"PR Number: {pr_number}")
        print(f"Repository: {repo_owner}/{repo_name}")
        print(f"Labels: {labels}")

    # Define GitHub API headers
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Function to get config from URL
    def get_config_from_url(url):
        try:
            print(f"Fetching config from URL: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching config from URL: {e}")
            return None

    # Always fetch from the backports URL
    config = get_config_from_url(backports_url)

    # Initialize target branches list
    target_branches = []

    # Extract branches from config if available
    if config and 'branches' in config:
        branches_data = config['branches']

        if isinstance(branches_data, str):
            # If branches is a string with space-separated values, split it
            target_branches = [b for b in branches_data.split() if b]
        elif isinstance(branches_data, list):
            # If branches is an array, use it directly
            target_branches = branches_data

        print(f"Found branches in config: {target_branches}")
    else:
        print("No branches found in config or config not available")

    # Filter branches based on the labels
    filtered_branches = []

    # Check if backport-active-all is present (takes precedence)
    if 'backport-active-all' in labels:
        # Use all branches from the JSON, but exclude 'main'
        filtered_branches = [branch for branch in target_branches if branch != 'main']
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
    if filtered_branches:
        comment = f"@mergifyio backport {' '.join(filtered_branches)}"

        # Create comment via GitHub API
        comment_url = f"{github_api_url}/repos/{repo_owner}/{repo_name}/issues/{pr_number}/comments"
        comment_data = {"body": comment}

        # Comment will be posted as the GitHub Actions bot
        print("Using GitHub token for authentication - comment will be posted as the GitHub Actions bot")

        if test_mode:
            print(f"TEST MODE: Would post comment to PR #{pr_number}: {comment}")
            print(f"TEST MODE: API URL would be: {comment_url}")
            success = True
        else:
            response = requests.post(comment_url, headers=headers, json=comment_data)
            
            if response.status_code == 201:
                print(f"Successfully added backport comment: {comment}")
                success = True
            else:
                print(f"Failed to add comment. Status code: {response.status_code}")
                print(f"Response: {response.text}")
                success = False

        # Return success code for CI
        return 0 if success else 1
    else:
        print("No branches to backport to after filtering")
        return 0

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
