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
from datetime import datetime, timedelta, timezone

# API Constants
API_BASE_URL = "https://api.buildkite.com/v2"
FLAKY_TESTS_ENDPOINT = "/analytics/organizations/{org}/suites/{suite}/flaky-tests"
TESTS_ENDPOINT = "/analytics/organizations/{org}/suites/{suite}/tests"
FLAKY_LABEL = "flaky"
GITHUB_FLAKY_LABEL = "flaky-test"
ISSUE_TITLE_PREFIX = "[Flaky Test]"

# Default values
DEFAULT_UNKNOWN = "Unknown"
DEFAULT_NA = "N/A"
DEFAULT_EMPTY = ""


class BuildkiteTestEngineClient:
    """Client for interacting with Buildkite Test Engine REST API."""

    def __init__(self, api_token: str, org_slug: str):
        self.api_token = api_token
        self.org_slug = org_slug
        self.headers = {"Authorization": f"Bearer {api_token}"}

    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Any:
        url = f"{API_BASE_URL}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params or {})
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _parse_iso_timestamp(timestamp: str) -> datetime:
        """Parse ISO 8601 timestamp, handling Z suffix."""
        return datetime.fromisoformat(timestamp.replace('Z', '+00:00'))

    def get_flaky_tests(
        self,
        suite_id: str,
        branch: Optional[str] = None,
        per_page: int = 100,
        days: Optional[int] = None,
        use_deprecated_endpoint: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Get flaky tests for a test suite.

        Note: Date filtering only works with deprecated endpoint (has timestamp fields).
        """
        endpoint_template = FLAKY_TESTS_ENDPOINT if use_deprecated_endpoint else TESTS_ENDPOINT
        endpoint = endpoint_template.format(org=self.org_slug, suite=suite_id)

        params = {
            "per_page": per_page,
            **({} if use_deprecated_endpoint else {"label": FLAKY_LABEL}),
            **({"branch": branch} if branch else {})
        }

        all_tests = self._fetch_paginated(endpoint, params, per_page)

        if days and use_deprecated_endpoint:
            return self._filter_by_days(all_tests, days)
        elif days and not use_deprecated_endpoint:
            print("Warning: Cannot filter by days with current endpoint (no timestamp fields)")

        return all_tests

    def _fetch_paginated(self, endpoint: str, params: Dict, per_page: int) -> List[Dict[str, Any]]:
        """Fetch all pages of results from API."""
        all_tests = []
        page = 1

        while True:
            params["page"] = page
            tests = self._make_request(endpoint, params)
            if not tests or len(tests) < per_page:
                all_tests.extend(tests)
                break
            all_tests.extend(tests)
            page += 1

        return all_tests

    def _filter_by_days(self, tests: List[Dict[str, Any]], days: int) -> List[Dict[str, Any]]:
        """Filter tests to those occurring in the last N days."""
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
        filtered = []

        for test in tests:
            if latest_occurrence := test.get("latest_occurrence_at"):
                try:
                    if self._parse_iso_timestamp(latest_occurrence) >= cutoff_date:
                        filtered.append(test)
                except (ValueError, AttributeError):
                    filtered.append(test)  # Include on parse error
            else:
                filtered.append(test)  # Include if no timestamp

        if len(tests) > len(filtered):
            print(f"Filtered {len(tests) - len(filtered)} test(s) older than {days} days (showing {len(filtered)} recent)")

        return filtered


class GitHubIssueManager:
    """Manages GitHub issues for flaky tests."""

    def __init__(self, repo: str):
        self.repo = repo
        self._existing_issues_cache = None

    def _run_gh_command(self, args: List[str]) -> str:
        result = subprocess.run(
            ["gh"] + args,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()

    @staticmethod
    def _format_issue_title(test_name: str, scope: str) -> str:
        """Format standardized issue title."""
        return f"{ISSUE_TITLE_PREFIX} {scope} {test_name}"

    @staticmethod
    def _extract_test_info(test_data: Dict[str, Any]) -> tuple[str, str, str, str]:
        """Extract common test fields with defaults."""
        return (
            test_data.get("name", DEFAULT_UNKNOWN),
            test_data.get("scope", DEFAULT_EMPTY),
            test_data.get("location", DEFAULT_NA),
            test_data.get("web_url", DEFAULT_EMPTY)
        )

    @staticmethod
    def _build_markdown(heading: str, fields: Dict[str, Any], test_data: Dict[str, Any]) -> str:
        """Build markdown with fields and JSON data."""
        lines = [f"## {heading}\n"]
        lines.extend(f"* **{k}:** {v}" for k, v in fields.items())
        lines.extend(["\n### Details\n", "```json", json.dumps(test_data, indent=2), "```"])
        return "\n".join(lines)

    def _load_existing_issues(self) -> None:
        """Load all existing flaky-test issues once to avoid N+1 queries."""
        if self._existing_issues_cache is not None:
            return

        try:
            output = self._run_gh_command([
                "issue", "list",
                "--repo", self.repo,
                "--label", GITHUB_FLAKY_LABEL,
                "--json", "number,title,state,url",
                "--limit", "1000"
            ])
            self._existing_issues_cache = json.loads(output) if output else []
        except Exception as e:
            print(f"Warning: Could not load existing issues: {e}", file=sys.stderr)
            self._existing_issues_cache = []

    def search_existing_issue(self, test_name: str, scope: str) -> Optional[Dict[str, Any]]:
        """Search for an existing GitHub issue for this test in cached issues."""
        self._load_existing_issues()
        title = self._format_issue_title(test_name, scope)

        for issue in self._existing_issues_cache:
            if issue["title"] == title or test_name in issue["title"]:
                return issue

        return None

    def create_issue(self, test_data: Dict[str, Any]) -> Optional[str]:
        """Create a new GitHub issue for a flaky test."""
        test_name, scope, location, web_url = self._extract_test_info(test_data)
        title = self._format_issue_title(test_name, scope)

        fields = {
            "Test Name": test_name,
            "Scope": scope,
            "Location": location,
            "Buildkite Link": web_url
        }

        if "instances" in test_data:
            fields["Flaky Instances"] = test_data['instances']
            fields["Latest Occurrence"] = test_data.get('latest_occurrence_at', DEFAULT_NA)

        body = self._build_markdown("Flaky Test", fields, test_data)

        try:
            return self._run_gh_command([
                "issue", "create",
                "--repo", self.repo,
                "--title", title,
                "--body", body,
                "--label", GITHUB_FLAKY_LABEL
            ])
        except Exception as e:
            print(f"Error creating GitHub issue: {e}", file=sys.stderr)
            return None

    def add_comment(self, issue_number: int, test_data: Dict[str, Any]) -> bool:
        """Add a comment to an existing GitHub issue."""
        fields = {
            "Latest Occurrence": test_data.get("latest_occurrence_at", DEFAULT_NA),
            "Total Instances": test_data.get("instances", DEFAULT_NA),
            "Buildkite Link": test_data.get("web_url", DEFAULT_EMPTY)
        }

        comment = self._build_markdown("Flaky Test Still Occurring", fields, test_data)

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
        """Process a flaky test: create issue or add comment to existing."""
        test_name, scope, _, _ = self._extract_test_info(test_data)
        existing = self.search_existing_issue(test_name, scope)

        if not existing or existing["state"] == "CLOSED":
            issue_url = self.create_issue(test_data)
            if issue_url:
                msg = f"Created new issue: {issue_url}"
                if existing:
                    msg = f"Created new issue (previous #{existing['number']} was closed): {issue_url}"
                return (msg, True)
            return ("Failed to create issue", False)

        # Issue is open, add comment
        if self.add_comment(existing["number"], test_data):
            return (f"Added comment to existing issue #{existing['number']}: {existing['url']}", False)
        return (f"Failed to add comment to issue #{existing['number']}", False)


def _sanitize_filename(name: str, max_length: int = 200) -> str:
    """Sanitize filename by replacing unsafe characters."""
    allowed_chars = {'-', '_', '.'}
    safe = "".join(c if c.isalnum() or c in allowed_chars else '_' for c in name)
    return safe[:max_length]


def save_flaky_test_to_file(test_data: Dict[str, Any], output_dir: Path, index: int) -> str:
    """Save flaky test data to a JSON file."""
    output_dir.mkdir(parents=True, exist_ok=True)

    test_identifier = test_data.get("identifier") or test_data.get("name") or f"test_{index}"
    safe_name = _sanitize_filename(test_identifier)
    filepath = output_dir / f"flaky_test_{index:03d}_{safe_name}.json"

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

    if args.create_github_issues and not args.github_repo:
        print("Error: --github-repo is required when --create-github-issues is specified", file=sys.stderr)
        sys.exit(1)

    if args.days and args.endpoint == "current":
        print("Warning: --days filtering is not supported with --endpoint current", file=sys.stderr)
        print("         The 'current' endpoint doesn't provide timestamp fields.", file=sys.stderr)
        print("         Use --endpoint deprecated (default) for date-based filtering.", file=sys.stderr)
        print("", file=sys.stderr)

    output_dir = Path(args.output_dir)
    github_manager = GitHubIssueManager(args.github_repo) if args.create_github_issues else None

    if github_manager:
        print(f"GitHub integration enabled for repository: {args.github_repo}")

    try:
        print(f"Connecting to Buildkite Test Engine for organization: {args.org}")
        client = BuildkiteTestEngineClient(args.api_token, args.org)

        print(f"Fetching flaky tests from suite: {args.suite_id}")
        print(f"Using endpoint: {args.endpoint}")
        if args.branch:
            print(f"Branch filter: {args.branch}")
        if args.days:
            print(f"Time filter: Last {args.days} days")

        flaky_tests = client.get_flaky_tests(
            args.suite_id,
            args.branch,
            args.per_page,
            args.days,
            args.endpoint == "deprecated"
        )

        if not flaky_tests:
            print("\nNo flaky tests detected!")
            if args.days:
                print(f"(No tests were flaky in the last {args.days} days)")
            return

        print(f"\nFound {len(flaky_tests)} flaky test(s):")
        print("-" * 80)

        issues_created = 0
        use_deprecated = args.endpoint == "deprecated"

        for idx, test_data in enumerate(flaky_tests, start=1):
            filepath = save_flaky_test_to_file(test_data, output_dir, idx)

            test_name = test_data.get("name") or test_data.get("identifier", DEFAULT_UNKNOWN)
            print(f"\n[{idx}/{len(flaky_tests)}] Test: {test_name}")
            print(f"  Location: {test_data.get('location', DEFAULT_NA)}")

            if use_deprecated and 'instances' in test_data:
                print(f"  Flaky instances: {test_data.get('instances', DEFAULT_NA)}")
                print(f"  Latest occurrence: {test_data.get('latest_occurrence_at', DEFAULT_NA)}")
                if resolved := test_data.get('last_resolved_at'):
                    print(f"  Last resolved: {resolved}")

            print(f"  Saved to: {filepath}")

            if github_manager:
                print(f"  Processing GitHub issue...", end=" ")
                status, was_created = github_manager.process_flaky_test(test_data)
                print(status)

                if was_created:
                    issues_created += 1
                    if args.max_issues and issues_created >= args.max_issues:
                        print(f"\nReached maximum of {args.max_issues} issue(s) created. Stopping.")
                        print(f"Processed {idx} of {len(flaky_tests)} flaky tests.")
                        break

        print("\n" + "-" * 80)
        print(f"\nAll flaky test reports saved to: {output_dir}")

        if github_manager and issues_created > 0:
            print(f"\nGitHub Summary:")
            print(f"  New issues created: {issues_created}")
            if args.max_issues:
                print(f"  Issue creation limit: {args.max_issues}")

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
