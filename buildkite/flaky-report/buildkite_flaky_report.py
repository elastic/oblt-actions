#!/usr/bin/env python3
"""
Buildkite Test Engine Flaky Test Detector

This script queries the Buildkite Test Engine API to detect flaky tests
for a given test suite and creates a JSON file for each flaky test found.

Requirements:
- Python 3.13+
- requests library (pip install requests)

Environment Variables:
- BUILDKITE_API_TOKEN: Your Buildkite API access token
- BUILDKITE_ORG_SLUG: Your organization slug
"""

import logging
import os
import sys
import json
import argparse
import subprocess
from typing import List, Dict, Any, Optional
from pathlib import Path
import requests
from datetime import datetime, timedelta, timezone

logger = logging.getLogger(__name__)

# API Constants
API_BASE_URL = "https://api.buildkite.com/v2"
FLAKY_TESTS_ENDPOINT = "/analytics/organizations/{org}/suites/{suite}/flaky-tests"
TESTS_ENDPOINT = "/analytics/organizations/{org}/suites/{suite}/tests"
RUNS_ENDPOINT = "/analytics/organizations/{org}/suites/{suite}/runs"
FAILED_EXECUTIONS_ENDPOINT = "/analytics/organizations/{org}/suites/{suite}/runs/{run_id}/failed_executions"
FLAKY_LABEL = "flaky"
DEFAULT_TIMEOUT = 30  # seconds

# Default values
DEFAULT_UNKNOWN = "Unknown"
DEFAULT_NA = "N/A"
DEFAULT_EMPTY = ""


class BuildkiteTestEngineClient:
    """Client for interacting with Buildkite Test Engine REST API."""

    def __init__(self, api_token: str, org_slug: str, timeout: int = DEFAULT_TIMEOUT):
        self.api_token = api_token
        self.org_slug = org_slug
        self.timeout = timeout
        self.headers = {"Authorization": f"Bearer {api_token}"}

    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Any:
        url = f"{API_BASE_URL}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params or {}, timeout=self.timeout)
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

        if days is not None and use_deprecated_endpoint:
            return self._filter_by_days(all_tests, days)
        elif days is not None and not use_deprecated_endpoint:
            logger.warning("Cannot filter by days with current endpoint (no timestamp fields)")

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
            logger.info("Filtered %d test(s) older than %d days (showing %d recent)",
                        len(tests) - len(filtered), days, len(filtered))

        return filtered

    def get_recent_runs(self, suite_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get recent runs for a test suite.

        Args:
            suite_id: Test suite ID
            limit: Maximum number of runs to fetch (default: 50)

        Returns:
            List of run objects (up to limit)
        """
        endpoint = RUNS_ENDPOINT.format(org=self.org_slug, suite=suite_id)

        # Use pagination to fetch up to limit runs
        # API page size is typically capped at 100
        per_page = min(limit, 100)

        all_runs = []
        page = 1

        while len(all_runs) < limit:
            # Create new params dict for each request to avoid mutation issues
            params = {"per_page": per_page, "page": page}
            runs = self._make_request(endpoint, params)

            if not runs:
                break

            all_runs.extend(runs)

            # Stop if we got fewer results than requested (last page)
            if len(runs) < per_page:
                break

            page += 1

        # Return only up to limit
        return all_runs[:limit]

    def get_failed_executions(self, suite_id: str, run_id: str) -> List[Dict[str, Any]]:
        """
        Get failed executions for a specific run.

        Args:
            suite_id: Test suite ID
            run_id: Run ID

        Returns:
            List of failed execution objects with failure_reason, failure_expanded, and test_id
        """
        endpoint = FAILED_EXECUTIONS_ENDPOINT.format(
            org=self.org_slug,
            suite=suite_id,
            run_id=run_id
        )
        # Request expanded failures to get full stack traces
        params = {"include_failure_expanded": "true"}
        try:
            return self._make_request(endpoint, params)
        except Exception as e:
            logger.debug("Failed to fetch executions for run %s: %s", run_id, e)
            return []

    @staticmethod
    def _extract_failure_message(execution: Dict[str, Any]) -> Optional[List[str]]:
        """
        Extract failure message from a failed execution.

        Prioritizes failure_expanded (full trace) over failure_reason (truncated).

        Args:
            execution: Failed execution object from API

        Returns:
            List of strings (one per line) or None if no failure info available
        """
        # Priority 1: failure_expanded (array of objects with backtrace field)
        if failure_expanded := execution.get("failure_expanded"):
            if isinstance(failure_expanded, list) and failure_expanded:
                first_item = failure_expanded[0]
                if isinstance(first_item, dict):
                    if backtrace := first_item.get("backtrace"):
                        if isinstance(backtrace, list):
                            # Keep as list of strings
                            return [str(line) for line in backtrace]

        # Priority 2: failure_reason (truncated to 1024 chars)
        if failure_reason := execution.get("failure_reason"):
            if isinstance(failure_reason, str) and failure_reason.strip():
                # Split into lines for consistency
                return failure_reason.strip().split('\n')

        return None

    @staticmethod
    def _is_duplicate_failure(
        failure_lines: List[str],
        existing_failures: List[Dict[str, Any]],
        signature_lines: int = 10,
        signature_chars: int = 500
    ) -> bool:
        """
        Check if a failure is a duplicate of existing failures.

        Args:
            failure_lines: New failure message as list of strings
            existing_failures: List of existing failure examples
            signature_lines: Number of lines to use for signature (default: 10)
            signature_chars: Number of chars to use for signature (default: 500)

        Returns:
            True if duplicate, False otherwise
        """
        # Create signature from first few lines
        failure_signature = '\n'.join(failure_lines[:signature_lines])[:signature_chars]

        # Check if we already have a similar failure
        return any(
            '\n'.join(existing.get("message", [])[:signature_lines])[:signature_chars] == failure_signature
            for existing in existing_failures
        )

    def enrich_flaky_tests_with_failures(
        self,
        suite_id: str,
        flaky_tests: List[Dict[str, Any]],
        max_runs: int = 50,
        max_examples_per_test: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Enrich flaky test data with failure reasons from recent runs.

        Args:
            suite_id: Test suite ID
            flaky_tests: List of flaky test objects
            max_runs: Maximum number of runs to check (default: 50, 0 to disable)
            max_examples_per_test: Maximum failure examples to collect per test (default: 5)

        Returns:
            Flaky tests enriched with failure_examples field (list of dicts with 'message', 'run_url', 'run_time')
        """
        # Initialize failure_examples field for each test
        for test in flaky_tests:
            test["failure_examples"] = []

        # Skip enrichment if max_runs is 0
        if max_runs == 0:
            logger.info("Skipping failure enrichment (max_runs=0)")
            return flaky_tests

        logger.info("Fetching failure details from recent runs...")

        # Create a map of test_id -> test for quick lookup
        test_map = {test.get("id"): test for test in flaky_tests if test.get("id")}

        # Fetch recent runs
        runs = self.get_recent_runs(suite_id, limit=max_runs)
        logger.info("Checking %d recent runs for failure details", len(runs))

        # For each run, fetch failed executions
        for run_idx, run in enumerate(runs):
            # Check if all tests have reached their cap - short circuit to avoid unnecessary API calls
            if all(len(test.get("failure_examples", [])) >= max_examples_per_test for test in flaky_tests):
                logger.info("All tests have %d examples, stopping early after %d runs",
                           max_examples_per_test, run_idx)
                break

            run_id = run.get("id")
            if not run_id:
                continue

            failed_executions = self.get_failed_executions(suite_id, run_id)

            # Match failures to flaky tests
            for idx, execution in enumerate(failed_executions):
                # Debug: log available fields in first execution
                if idx == 0 and failed_executions and logger.isEnabledFor(logging.DEBUG):
                    logger.debug("Failed execution fields available: %s", list(execution.keys()))
                    logger.debug("Sample execution data: %s", json.dumps(execution, indent=2))

                test_id = execution.get("test_id")
                if test_id not in test_map:
                    continue

                test = test_map[test_id]

                # Skip if test already has max examples
                if len(test["failure_examples"]) >= max_examples_per_test:
                    continue

                # Extract failure message using helper method
                failure_message_lines = self._extract_failure_message(execution)
                if not failure_message_lines:
                    continue

                # Skip if duplicate using helper method
                if self._is_duplicate_failure(failure_message_lines, test["failure_examples"]):
                    continue

                # Create and add failure example
                failure_example = {
                    "message": failure_message_lines,
                    "run_url": run.get("url"),
                    "run_time": run.get("created_at")
                }
                test["failure_examples"].append(failure_example)

                logger.debug("Added failure example for %s (%d/%d)",
                           test.get("name"), len(test["failure_examples"]), max_examples_per_test)

        # Log summary
        tests_with_failures = sum(1 for t in flaky_tests if t.get("failure_examples"))
        logger.info("Found failure details for %d/%d flaky tests", tests_with_failures, len(flaky_tests))

        return flaky_tests


class GitHubIssueManager:
    """Manages GitHub issues for flaky tests."""

    def __init__(self, repo: str, issue_title_prefix: str = "", github_label: Optional[str] = None):
        self.repo = repo
        self.issue_title_prefix = issue_title_prefix
        self.github_label = github_label
        self._existing_issues_cache = None

    def _run_gh_command(self, args: List[str]) -> str:
        result = subprocess.run(
            ["gh"] + args,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()

    def _format_issue_title(self, test_name: str, scope: str) -> str:
        """Format standardized issue title."""
        if self.issue_title_prefix:
            return f"{self.issue_title_prefix} {scope} {test_name}"
        return f"{scope} {test_name}"

    @staticmethod
    def _extract_test_info(test_data: Dict[str, Any]) -> tuple[str, str, str, str, str]:
        """
        Extract common test fields with defaults.

        Note: file_name and location may be null for tests recorded by older collector versions.
        They should backfill automatically on the next run.
        """
        return (
            test_data.get("name", DEFAULT_UNKNOWN),
            test_data.get("scope", DEFAULT_EMPTY),
            test_data.get("location") or DEFAULT_NA,
            test_data.get("file_name") or DEFAULT_NA,
            test_data.get("web_url", DEFAULT_EMPTY)
        )

    @staticmethod
    def _build_markdown(heading: str, fields: Dict[str, Any], test_data: Dict[str, Any]) -> str:
        """Build markdown with fields and JSON data (sanitized to prevent huge bodies)."""
        lines = [f"## {heading}\n"]
        lines.extend(f"* **{k}:** {v}" for k, v in fields.items())

        # Sanitize test_data to prevent huge issue bodies
        sanitized_data = test_data.copy()

        # Remove or truncate failure_examples to avoid bloat
        if "failure_examples" in sanitized_data:
            examples = sanitized_data["failure_examples"]
            if isinstance(examples, list) and len(examples) > 0:
                # Keep only count in the JSON details section
                sanitized_data["failure_examples_count"] = len(examples)
                del sanitized_data["failure_examples"]

        lines.extend(["\n### Details\n", "```json", json.dumps(sanitized_data, indent=2), "```"])
        return "\n".join(lines)

    def _load_existing_issues(self) -> None:
        """Load all existing flaky-test issues once to avoid N+1 queries."""
        if self._existing_issues_cache is not None:
            return

        try:
            cmd = [
                "issue", "list",
                "--repo", self.repo,
                "--json", "number,title,state,url",
                "--limit", "1000"
            ]

            # Only add label filter if label is provided
            if self.github_label:
                cmd.extend(["--label", self.github_label])

            output = self._run_gh_command(cmd)
            self._existing_issues_cache = json.loads(output) if output else []
        except Exception as e:
            logger.warning("Could not load existing issues: %s", e)
            self._existing_issues_cache = []

    def search_existing_issue(self, test_name: str, scope: str) -> Optional[Dict[str, Any]]:
        """Search for an existing GitHub issue for this test in cached issues."""
        self._load_existing_issues()
        title = self._format_issue_title(test_name, scope)

        for issue in self._existing_issues_cache:
            if title in issue["title"]:
                return issue

        return None

    @staticmethod
    def _format_failure_examples_markdown(failure_examples: List, max_examples: int = 3) -> str:
        """
        Format failure examples as markdown for GitHub issue.

        Args:
            failure_examples: List of failure examples (dicts or strings)
            max_examples: Maximum number of examples to include (default: 3)

        Returns:
            Formatted markdown string for failure examples section
        """
        if not failure_examples:
            return ""

        parts = ["\n\n### Failure Examples\n"]

        for idx, failure in enumerate(failure_examples[:max_examples], 1):
            parts.append(f"\n**Example {idx}:**\n")

            # Extract metadata and message
            if isinstance(failure, dict):
                if run_url := failure.get("run_url"):
                    parts.append(f"**Run:** {run_url}\n")
                if run_time := failure.get("run_time"):
                    parts.append(f"**Time:** {run_time}\n")
                failure_msg = failure.get("message", "")
            else:
                # Backward compatibility if failure is a string
                failure_msg = failure

            # Add failure message in code block
            parts.append("**Stacktrace:**\n")
            parts.append("\n```\n")
            if isinstance(failure_msg, list):
                # List of strings - join with newlines
                parts.append("\n".join(failure_msg))
            else:
                # String (backward compatibility)
                parts.append(str(failure_msg))
            parts.append("\n```\n")

        return "".join(parts)

    def create_issue(self, test_data: Dict[str, Any]) -> Optional[str]:
        """Create a new GitHub issue for a flaky test."""
        test_name, scope, location, file_name, web_url = self._extract_test_info(test_data)
        title = self._format_issue_title(test_name, scope)

        fields = {
            "Test Name": test_name,
            "Scope": scope,
            "File": file_name,
            "Location": location,
            "Buildkite Link": web_url
        }

        if "instances" in test_data:
            fields["Flaky Instances"] = test_data['instances']
            fields["Latest Occurrence"] = test_data.get('latest_occurrence_at', DEFAULT_NA)

        # Build base markdown
        body_parts = [self._build_markdown("Flaky Test", fields, test_data)]

        # Add failure examples if available
        if failure_examples := test_data.get("failure_examples"):
            logger.debug("Adding %d failure examples to issue", len(failure_examples))
            body_parts.append(self._format_failure_examples_markdown(failure_examples))
        else:
            logger.debug("No failure examples found for test: %s", test_name)

        body = "".join(body_parts)

        try:
            cmd = [
                "issue", "create",
                "--repo", self.repo,
                "--title", title,
                "--body", body
            ]

            # Only add label if provided
            if self.github_label:
                cmd.extend(["--label", self.github_label])

            return self._run_gh_command(cmd)
        except Exception as e:
            logger.error("Error creating GitHub issue: %s", e)
            return None

    def add_comment(self, issue_number: int, test_data: Dict[str, Any]) -> bool:
        """Add a comment to an existing GitHub issue."""
        fields = {
            "Latest Occurrence": test_data.get("latest_occurrence_at", DEFAULT_NA),
            "Total Instances": test_data.get("instances", DEFAULT_NA),
            "Buildkite Link": test_data.get("web_url", DEFAULT_EMPTY)
        }

        comment_parts = [self._build_markdown("Flaky Test Still Occurring", fields, test_data)]

        # Add recent failure examples if available (limit to 1 for comments to avoid huge updates)
        if failure_examples := test_data.get("failure_examples"):
            logger.debug("Adding recent failure example to comment")
            comment_parts.append(self._format_failure_examples_markdown(failure_examples, max_examples=1))

        comment = "".join(comment_parts)

        try:
            self._run_gh_command([
                "issue", "comment", str(issue_number),
                "--repo", self.repo,
                "--body", comment
            ])
            return True
        except Exception as e:
            logger.error("Error adding comment to issue #%d: %s", issue_number, e)
            return False

    def process_flaky_test(self, test_data: Dict[str, Any]) -> tuple[str, bool]:
        """Process a flaky test: create issue or add comment to existing."""
        test_name, scope, _, _, _ = self._extract_test_info(test_data)
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


def create_arg_parser() -> argparse.ArgumentParser:
    """Create and return the argument parser for the CLI."""
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
        default=1
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
        help="GitHub repository in format 'owner/repo' (e.g., 'elastic/beats'). Required when --create-github-issues is specified.",
        default=None
    )
    parser.add_argument(
        "--max-issues",
        help="Maximum number of new GitHub issues to create (limits issue creation only, not test detection; default: no limit)",
        type=int,
        default=None
    )
    parser.add_argument(
        "--github-issue-title-prefix",
        help="Prefix for GitHub issue titles (default: empty, no prefix)",
        default=""
    )
    parser.add_argument(
        "--github-label",
        help="Label to apply to GitHub issues (default: none)",
        default=""
    )
    parser.add_argument(
        "--max-runs",
        help="Maximum number of recent runs to check for failure details (default: 50)",
        type=int,
        default=50
    )
    parser.add_argument(
        "--debug",
        help="Enable debug logging to see API response details",
        action="store_true"
    )
    return parser


def validate_args(args: argparse.Namespace) -> None:
    """Validate parsed arguments, exiting with error messages on invalid input."""
    if not args.api_token:
        logger.error("API token is required. Set BUILDKITE_API_TOKEN or use --api-token")
        sys.exit(1)

    if not args.org:
        logger.error("Organization slug is required. Set BUILDKITE_ORG_SLUG or use --org")
        sys.exit(1)

    if args.days is not None and args.days < 0:
        logger.error("--days must be >= 0")
        sys.exit(1)

    if args.max_issues is not None and args.max_issues < 0:
        logger.error("--max-issues must be >= 0")
        sys.exit(1)

    if args.max_runs < 0:
        logger.error("--max-runs must be >= 0")
        sys.exit(1)

    if args.create_github_issues and not args.github_repo:
        logger.error("--github-repo is required when --create-github-issues is specified")
        sys.exit(1)

    if args.days is not None and args.endpoint == "current":
        logger.warning("--days filtering is not supported with --endpoint current")
        logger.warning("The 'current' endpoint doesn't provide timestamp fields.")
        logger.warning("Use --endpoint deprecated (default) for date-based filtering.")


def main():
    """Main entry point for the script."""
    parser = create_arg_parser()
    args = parser.parse_args()

    # Set logging level based on debug flag
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=log_level, format="%(levelname)s: %(message)s" if args.debug else "%(message)s")

    validate_args(args)

    output_dir = Path(args.output_dir)

    # Create GitHub manager with custom settings
    github_manager = None
    if args.create_github_issues:
        # Treat empty string as None for label
        github_label = args.github_label if args.github_label else None
        github_manager = GitHubIssueManager(
            args.github_repo,
            issue_title_prefix=args.github_issue_title_prefix,
            github_label=github_label
        )
        logger.info("GitHub integration enabled for repository: %s", args.github_repo)
        if args.github_issue_title_prefix:
            logger.info("  Issue title prefix: '%s'", args.github_issue_title_prefix)
        else:
            logger.info("  Issue title prefix: (none)")
        if github_label:
            logger.info("  GitHub label: '%s'", github_label)
        else:
            logger.info("  GitHub label: (none)")

    try:
        logger.info("Connecting to Buildkite Test Engine for organization: %s", args.org)
        client = BuildkiteTestEngineClient(args.api_token, args.org)

        logger.info("Fetching flaky tests from suite: %s", args.suite_id)
        logger.info("Using endpoint: %s", args.endpoint)
        if args.branch:
            logger.info("Branch filter: %s", args.branch)
        if args.days is not None:
            logger.info("Time filter: Last %d days", args.days)

        flaky_tests = client.get_flaky_tests(
            args.suite_id,
            args.branch,
            args.per_page,
            args.days,
            args.endpoint == "deprecated"
        )

        if not flaky_tests:
            logger.info("\nNo flaky tests detected!")
            if args.days is not None:
                logger.info("(No tests were flaky in the last %d days)", args.days)
            return

        # Enrich with failure details from recent runs (if possible)
        try:
            flaky_tests = client.enrich_flaky_tests_with_failures(
                args.suite_id,
                flaky_tests,
                max_runs=args.max_runs
            )
        except Exception as e:
            logger.warning("Could not fetch failure details: %s", e)
            # Continue without failure details
            for test in flaky_tests:
                test["failure_examples"] = []

        logger.info("\nFound %d flaky test(s):", len(flaky_tests))
        logger.info("-" * 80)

        issues_created = 0
        use_deprecated = args.endpoint == "deprecated"

        for idx, test_data in enumerate(flaky_tests, start=1):
            filepath = save_flaky_test_to_file(test_data, output_dir, idx)

            test_name = test_data.get("name") or test_data.get("identifier", DEFAULT_UNKNOWN)
            logger.info("\n[%d/%d] Test: %s", idx, len(flaky_tests), test_name)
            if file_name := test_data.get('file_name'):
                logger.info("  File: %s", file_name)
            logger.info("  Location: %s", test_data.get('location', DEFAULT_NA))
            if failure_count := len(test_data.get('failure_examples', [])):
                logger.info("  Failure examples found: %d", failure_count)

            if use_deprecated and 'instances' in test_data:
                logger.info("  Flaky instances: %s", test_data.get('instances', DEFAULT_NA))
                logger.info("  Latest occurrence: %s", test_data.get('latest_occurrence_at', DEFAULT_NA))
                if resolved := test_data.get('last_resolved_at'):
                    logger.info("  Last resolved: %s", resolved)

            logger.info("  Saved to: %s", filepath)

            if github_manager:
                # Check limit before processing
                if args.max_issues is not None and issues_created >= args.max_issues:
                    logger.info("  Skipping GitHub issue (limit of %d reached)", args.max_issues)
                else:
                    status, was_created = github_manager.process_flaky_test(test_data)
                    logger.info("  Processing GitHub issue... %s", status)

                    if was_created:
                        issues_created += 1

        logger.info("\n" + "-" * 80)
        logger.info("\nAll flaky test reports saved to: %s", output_dir)

        if github_manager:
            logger.info("\nGitHub Summary:")
            logger.info("  New issues created: %d", issues_created)
            if args.max_issues is not None:
                logger.info("  Issue creation limit: %d", args.max_issues)
                if issues_created >= args.max_issues and len(flaky_tests) > issues_created:
                    skipped = len(flaky_tests) - issues_created
                    logger.info("  Tests skipped (limit reached): %d", skipped)

    except requests.exceptions.HTTPError as e:
        logger.error("HTTP Error: %s", e)
        if hasattr(e, 'response'):
            logger.error("Response Status: %s", e.response.status_code)
            logger.error("Response: %s", e.response.text)
        sys.exit(1)
    except Exception as e:
        logger.error("Error: %s", e)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
