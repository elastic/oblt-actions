#!/usr/bin/env python3
"""
Buildkite Test Engine Flaky Test Detector

This script queries the Buildkite Test Engine API to detect flaky tests
for a given test suite and creates a JSON file for each flaky test found.

Requirements:
- Python 3.10+
- requests library (pip install requests)

Environment Variables:
- BUILDKITE_API_TOKEN: Your Buildkite API access token
- BUILDKITE_ORG_SLUG: Your organization slug
"""

import os
import sys
import json
import argparse
import subprocess
from typing import List, Dict, Any, Optional
from pathlib import Path
import requests
from datetime import datetime


class BuildkiteTestEngineClient:
    """Client for interacting with Buildkite Test Engine REST API."""

    def __init__(self, api_token: str, org_slug: str):
        """
        Initialize the Buildkite API client.

        Args:
            api_token: Buildkite API access token
            org_slug: Organization slug
        """
        self.api_token = api_token
        self.org_slug = org_slug
        self.base_url = "https://api.buildkite.com/v2"
        self.headers = {
            "Authorization": f"Bearer {api_token}"
        }

    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Any:
        """
        Make a GET request to the Buildkite REST API.

        Args:
            endpoint: API endpoint path
            params: Optional query parameters

        Returns:
            Response data from the API
        """
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params or {})
        response.raise_for_status()
        return response.json()

    def get_test_suite(self, suite_slug: str) -> Dict[str, Any]:
        """
        Get test suite information.

        Args:
            suite_slug: The test suite slug/identifier

        Returns:
            Test suite data
        """
        # Note: You may need to find the suite ID first
        # For now, we'll return the slug as-is
        return {"slug": suite_slug}

    def get_flaky_tests(
        self,
        suite_id: str,
        branch: Optional[str] = None,
        per_page: int = 100,
        days: Optional[int] = None,
        use_deprecated_endpoint: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Get flaky tests for a test suite using the REST API.

        Supports two endpoints:
        1. /flaky-tests (deprecated but richer data):
           - instances: Number of times the test was flaky
           - latest_occurrence_at: Timestamp of most recent flaky occurrence
           - most_recent_instance_at: Another timestamp reference
           - last_resolved_at: When flakiness was resolved (if ever)
           - ownership_team_ids: Team ownership information

        2. /tests?label=flaky (newer but minimal data):
           - Basic test info only: id, name, location, file_name, scope, labels

        Args:
            suite_id: The test suite ID
            branch: Optional branch filter
            per_page: Number of results per page (default: 100)
            days: Filter tests flaky in the last N days (optional, client-side filtering)
            use_deprecated_endpoint: If True, use /flaky-tests (default), else /tests?label=flaky

        Returns:
            List of flaky test data
        """
        if use_deprecated_endpoint:
            # Deprecated endpoint with richer data
            endpoint = f"/analytics/organizations/{self.org_slug}/suites/{suite_id}/flaky-tests"
            params = {"per_page": per_page}
        else:
            # Newer endpoint with minimal data
            endpoint = f"/analytics/organizations/{self.org_slug}/suites/{suite_id}/tests"
            params = {
                "label": "flaky",
                "per_page": per_page
            }

        if branch:
            params["branch"] = branch

        all_tests = []
        page = 1

        while True:
            params["page"] = page
            tests = self._make_request(endpoint, params)

            if not tests:
                break

            all_tests.extend(tests)

            # If we got fewer results than per_page, we've reached the end
            if len(tests) < per_page:
                break

            page += 1

        # Client-side filtering by days
        # Note: Only works with deprecated endpoint which has latest_occurrence_at field
        if days is not None:
            if not use_deprecated_endpoint:
                # Current endpoint doesn't have timestamp fields, can't filter by date
                print(f"Warning: Cannot filter by days with current endpoint (no timestamp fields available)")
                return all_tests

            from datetime import datetime, timedelta, timezone
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

            filtered_tests = []
            for test in all_tests:
                latest_occurrence = test.get("latest_occurrence_at")
                if latest_occurrence:
                    try:
                        # Parse ISO 8601 timestamp
                        occurrence_date = datetime.fromisoformat(latest_occurrence.replace('Z', '+00:00'))
                        if occurrence_date >= cutoff_date:
                            filtered_tests.append(test)
                    except (ValueError, AttributeError):
                        # If we can't parse the date, include the test to be safe
                        filtered_tests.append(test)
                else:
                    # If no timestamp, include the test
                    filtered_tests.append(test)

            total_count = len(all_tests)
            filtered_count = len(filtered_tests)
            if total_count > filtered_count:
                print(f"Filtered {total_count - filtered_count} test(s) older than {days} days (showing {filtered_count} recent)")

            return filtered_tests

        return all_tests


class GitHubIssueManager:
    """Manages GitHub issues for flaky tests."""

    def __init__(self, repo: str):
        """
        Initialize GitHub issue manager.

        Args:
            repo: GitHub repository in format 'owner/repo'
        """
        self.repo = repo

    def _run_gh_command(self, args: List[str]) -> str:
        """Run a gh CLI command and return the output."""
        try:
            result = subprocess.run(
                ["gh"] + args,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise Exception(f"gh command failed: {e.stderr}")

    def search_existing_issue(self, test_name: str, scope: str) -> Optional[Dict[str, Any]]:
        """
        Search for an existing GitHub issue for this test.

        Args:
            test_name: Name of the test
            scope: Scope of the test

        Returns:
            Issue data if found, None otherwise
        """
        # Create the title we expect
        title = f"[Flaky Test] {scope} {test_name}"

        # Search for issues with this title
        search_query = f'repo:{self.repo} in:title "{test_name}" label:flaky-test'

        try:
            output = self._run_gh_command([
                "issue", "list",
                "--repo", self.repo,
                "--search", search_query,
                "--json", "number,title,state,url",
                "--limit", "10"
            ])

            if not output:
                return None

            issues = json.loads(output)

            # Look for exact title match
            for issue in issues:
                if issue["title"] == title or test_name in issue["title"]:
                    return issue

            return None

        except Exception as e:
            print(f"Warning: Could not search for existing issue: {e}", file=sys.stderr)
            return None

    def create_issue(self, test_data: Dict[str, Any]) -> Optional[str]:
        """
        Create a new GitHub issue for a flaky test.

        Args:
            test_data: Flaky test data

        Returns:
            Issue URL if created, None otherwise
        """
        test_name = test_data.get("name", "Unknown")
        scope = test_data.get("scope", "")
        location = test_data.get("location", "N/A")
        web_url = test_data.get("web_url", "")

        # Create title
        title = f"[Flaky Test] {scope} {test_name}"

        # Create body
        body_parts = [
            "## Flaky Test\n",
            f"* **Test Name:** {test_name}",
            f"* **Scope:** {scope}",
            f"* **Location:** {location}",
            f"* **Buildkite Link:** {web_url}",
        ]

        # Add deprecated endpoint specific fields if available
        if "instances" in test_data:
            body_parts.append(f"* **Flaky Instances:** {test_data['instances']}")
            body_parts.append(f"* **Latest Occurrence:** {test_data.get('latest_occurrence_at', 'N/A')}")

        body_parts.append("\n### Details\n")
        body_parts.append("```json")
        body_parts.append(json.dumps(test_data, indent=2))
        body_parts.append("```")

        body = "\n".join(body_parts)

        try:
            output = self._run_gh_command([
                "issue", "create",
                "--repo", self.repo,
                "--title", title,
                "--body", body,
                "--label", "flaky-test"
            ])
            return output
        except Exception as e:
            print(f"Error creating GitHub issue: {e}", file=sys.stderr)
            return None

    def add_comment(self, issue_number: int, test_data: Dict[str, Any]) -> bool:
        """
        Add a comment to an existing GitHub issue.

        Args:
            issue_number: GitHub issue number
            test_data: Flaky test data

        Returns:
            True if comment added successfully, False otherwise
        """
        web_url = test_data.get("web_url", "")
        latest_occurrence = test_data.get("latest_occurrence_at", "N/A")
        instances = test_data.get("instances", "N/A")

        comment_parts = [
            f"## Flaky Test Still Occurring",
            f"",
            f"* **Latest Occurrence:** {latest_occurrence}",
            f"* **Total Instances:** {instances}",
            f"* **Buildkite Link:** {web_url}",
            f"",
            f"### Test Data",
            f"",
            f"```json",
            json.dumps(test_data, indent=2),
            f"```"
        ]

        comment = "\n".join(comment_parts)

        try:
            self._run_gh_command([
                "issue", "comment", str(issue_number),
                "--repo", self.repo,
                "--body", comment
            ])
            return True
        except Exception as e:
            print(f"Error adding comment to issue #{issue_number}: {e}", file=sys.stderr)
            return False

    def process_flaky_test(self, test_data: Dict[str, Any]) -> tuple[str, bool]:
        """
        Process a flaky test and create or update GitHub issue.

        Args:
            test_data: Flaky test data

        Returns:
            Tuple of (status message, was_created) where was_created is True if a new issue was created
        """
        test_name = test_data.get("name", "Unknown")
        scope = test_data.get("scope", "")

        # Search for existing issue
        existing_issue = self.search_existing_issue(test_name, scope)

        if existing_issue is None:
            # No issue exists, create a new one
            issue_url = self.create_issue(test_data)
            if issue_url:
                return (f"Created new issue: {issue_url}", True)
            else:
                return ("Failed to create issue", False)

        elif existing_issue["state"] == "CLOSED":
            # Issue exists but is closed, create a new one
            issue_url = self.create_issue(test_data)
            if issue_url:
                return (f"Created new issue (previous #{existing_issue['number']} was closed): {issue_url}", True)
            else:
                return (f"Failed to create issue (previous #{existing_issue['number']} was closed)", False)

        else:
            # Issue is open, add a comment
            success = self.add_comment(existing_issue["number"], test_data)
            if success:
                return (f"Added comment to existing issue #{existing_issue['number']}: {existing_issue['url']}", False)
            else:
                return (f"Failed to add comment to issue #{existing_issue['number']}", False)


def save_flaky_test_to_file(test_data: Dict[str, Any], output_dir: Path, index: int) -> str:
    """
    Save flaky test data to a JSON file.

    Args:
        test_data: Flaky test data
        output_dir: Directory to save the file
        index: Index number for the test

    Returns:
        Path to the created file
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create a safe filename from test identifier or name
    test_identifier = test_data.get("identifier") or test_data.get("name") or f"test_{index}"
    safe_filename = "".join(c if c.isalnum() or c in ('-', '_', '.') else '_' for c in test_identifier)
    safe_filename = safe_filename[:200]  # Limit filename length

    # Use index to make unique
    filename = f"flaky_test_{index:03d}_{safe_filename}.json"

    filepath = output_dir / filename

    with open(filepath, 'w') as f:
        json.dump(test_data, f, indent=2)

    return str(filepath)


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Detect flaky tests in Buildkite Test Engine and save them as JSON files"
    )
    parser.add_argument(
        "suite_id",
        help="Test suite ID (e.g., the UUID from your suite URL)"
    )
    parser.add_argument(
        "--branch",
        help="Branch to filter tests by",
        default=None
    )
    parser.add_argument(
        "--output-dir",
        help="Directory to save JSON files (default: ./flaky_tests)",
        default="./flaky_tests"
    )
    parser.add_argument(
        "--org",
        help="Organization slug (can also be set via BUILDKITE_ORG_SLUG env var)",
        default=os.getenv("BUILDKITE_ORG_SLUG")
    )
    parser.add_argument(
        "--api-token",
        help="Buildkite API token (can also be set via BUILDKITE_API_TOKEN env var)",
        default=os.getenv("BUILDKITE_API_TOKEN")
    )
    parser.add_argument(
        "--per-page",
        help="Number of results per page (default: 100)",
        type=int,
        default=100
    )
    parser.add_argument(
        "--days",
        help="Only include tests that were flaky in the last N days (e.g., --days 7 for last week)",
        type=int,
        default=7
    )
    parser.add_argument(
        "--endpoint",
        help="API endpoint to use: 'deprecated' (default, richer data) or 'current' (minimal data)",
        choices=["deprecated", "current"],
        default="deprecated"
    )
    parser.add_argument(
        "--create-github-issues",
        help="Create or update GitHub issues for flaky tests",
        action="store_true"
    )
    parser.add_argument(
        "--github-repo",
        help="GitHub repository in format 'owner/repo' (e.g., 'elastic/beats')",
        default=None
    )
    parser.add_argument(
        "--max-issues",
        help="Maximum number of new GitHub issues to create before stopping (default: no limit)",
        type=int,
        default=None
    )

    args = parser.parse_args()

    # Validate required parameters
    if not args.api_token:
        print("Error: API token is required. Set BUILDKITE_API_TOKEN or use --api-token", file=sys.stderr)
        sys.exit(1)

    if not args.org:
        print("Error: Organization slug is required. Set BUILDKITE_ORG_SLUG or use --org", file=sys.stderr)
        sys.exit(1)

    # Validate GitHub options
    if args.create_github_issues and not args.github_repo:
        print("Error: --github-repo is required when --create-github-issues is specified", file=sys.stderr)
        sys.exit(1)

    # Warn about --days with current endpoint
    if args.days and args.endpoint == "current":
        print("Warning: --days filtering is not supported with --endpoint current", file=sys.stderr)
        print("         The 'current' endpoint doesn't provide timestamp fields.", file=sys.stderr)
        print("         Use --endpoint deprecated (default) for date-based filtering.", file=sys.stderr)
        print("", file=sys.stderr)

    output_dir = Path(args.output_dir)

    # Initialize GitHub manager if needed
    github_manager = None
    if args.create_github_issues:
        github_manager = GitHubIssueManager(args.github_repo)
        print(f"GitHub integration enabled for repository: {args.github_repo}")

    try:
        # Initialize client
        print(f"Connecting to Buildkite Test Engine for organization: {args.org}")
        client = BuildkiteTestEngineClient(args.api_token, args.org)

        # Get flaky tests
        print(f"Fetching flaky tests from suite: {args.suite_id}")
        print(f"Using endpoint: {args.endpoint}")
        if args.branch:
            print(f"Branch filter: {args.branch}")
        if args.days:
            print(f"Time filter: Last {args.days} days")

        use_deprecated = args.endpoint == "deprecated"
        flaky_tests = client.get_flaky_tests(args.suite_id, args.branch, args.per_page, args.days, use_deprecated)

        if not flaky_tests:
            print("\nNo flaky tests detected! 🎉")
            if args.days:
                print(f"(No tests were flaky in the last {args.days} days)")
            return

        # Save each flaky test to a file
        print(f"\nFound {len(flaky_tests)} flaky test(s):")
        print("-" * 80)

        issues_created = 0
        max_issues = args.max_issues

        for idx, test_data in enumerate(flaky_tests, start=1):
            filepath = save_flaky_test_to_file(test_data, output_dir, idx)

            test_name = test_data.get("name") or test_data.get("identifier", "Unknown")
            print(f"\n[{idx}/{len(flaky_tests)}] Test: {test_name}")
            print(f"  Location: {test_data.get('location', 'N/A')}")

            # Show additional info if using deprecated endpoint
            if use_deprecated and 'instances' in test_data:
                print(f"  Flaky instances: {test_data.get('instances', 'N/A')}")
                print(f"  Latest occurrence: {test_data.get('latest_occurrence_at', 'N/A')}")
                if test_data.get('last_resolved_at'):
                    print(f"  Last resolved: {test_data.get('last_resolved_at')}")

            print(f"  Saved to: {filepath}")

            # Create or update GitHub issue if enabled
            if github_manager:
                print(f"  Processing GitHub issue...", end=" ")
                status, was_created = github_manager.process_flaky_test(test_data)
                print(status)

                # Track created issues and check limit
                if was_created:
                    issues_created += 1
                    if max_issues is not None and issues_created >= max_issues:
                        print(f"\n⚠️  Reached maximum of {max_issues} issue(s) created. Stopping.")
                        print(f"   Processed {idx} of {len(flaky_tests)} flaky tests.")
                        break

        print("\n" + "-" * 80)
        print(f"\nAll flaky test reports saved to: {output_dir}")

        # Print GitHub summary if enabled
        if github_manager and issues_created > 0:
            print(f"\nGitHub Summary:")
            print(f"  New issues created: {issues_created}")
            if max_issues:
                print(f"  Issue creation limit: {max_issues}")

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}", file=sys.stderr)
        if hasattr(e, 'response'):
            print(f"Response Status: {e.response.status_code}", file=sys.stderr)
            print(f"Response: {e.response.text}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
