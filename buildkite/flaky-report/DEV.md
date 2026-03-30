# Buildkite Flaky Test Detector

This Python script queries the Buildkite Test Engine REST API to fetch flaky tests for a given test suite and creates a JSON file for each flaky test found.

## What is a Flaky Test?

Buildkite Test Engine automatically identifies and labels tests as "flaky" based on their execution history. This script retrieves those pre-identified flaky tests using the REST API's `label=flaky` filter.

## Prerequisites

- Python 3.13 or higher
- GH cli
- Buildkite account with Test Engine enabled
- Buildkite API access token with appropriate permissions

## Configuration

### Create a Buildkite API Token

1. Go to your Buildkite account: [https://buildkite.com/user/api-access-tokens](https://buildkite.com/user/api-access-tokens)
2. Click "New API Access Token"
3. Give it a description (e.g., "Flaky Test Detector")
4. Select the required scopes:
   - `read_suites` - Read test suites
   - `read_test_analytics` - Read test analytics/test engine data
5. Click "Create Token" and save the token securely

### Find Your Test Suite ID

1. Go to your Buildkite Test Engine dashboard
2. Navigate to the test suite you want to analyze
3. The suite ID is in the URL: `https://buildkite.com/organizations/YOUR_ORG/analytics/suites/SUITE_ID`
4. Copy the `SUITE_ID` (it's usually a UUID like `abc123-def456-...`)

### Set Environment Variables

```bash
export BUILDKITE_API_TOKEN="your-api-token-here"
export BUILDKITE_ORG_SLUG="your-organization-slug"
```

You can find your organization slug in your Buildkite URL:
`https://buildkite.com/YOUR_ORG_SLUG`

## Usage

### Basic Usage

```bash
python buildkite_flaky_report.py YOUR_SUITE_ID
```

### With Options

```bash
python buildkite_flaky_report.py YOUR_SUITE_ID \
  --branch main \
  --days 1 \
  --output-dir ./my_flaky_tests \
  --org my-organization \
  --api-token your-token \
  --per-page 50
```

### Command Line Options

- `suite_id` (required): The test suite ID (UUID from your suite URL)
- `--branch`: Branch to filter tests by
- `--days`: Only include tests that were flaky in the last N days (e.g., `--days 7` for last week, default: 1)
  - ⚠️ **Only works with `--endpoint deprecated`** (current endpoint has no timestamp fields)
- `--endpoint`: API endpoint to use (default: `deprecated`)
  - `deprecated` - Uses `/flaky-tests` endpoint with richer data (instances, timestamps, resolution status)
  - `current` - Uses `/tests?label=flaky` endpoint with minimal data (no date filtering)
- `--output-dir`: Directory to save JSON files (default: `./flaky_tests`)
- `--org`: Organization slug (overrides `BUILDKITE_ORG_SLUG` env var)
- `--api-token`: API token (overrides `BUILDKITE_API_TOKEN` env var)
- `--per-page`: Number of results per page for pagination (default: 100)
- `--create-github-issues`: Enable GitHub issue creation/updates for flaky tests
- `--github-repo`: GitHub repository in format `owner/repo` (required if `--create-github-issues` is used)
- `--max-issues`: Maximum number of new GitHub issues to create before stopping (default: no limit, e.g., `--max-issues 2`)
- `--github-issue-title-prefix`: Prefix for GitHub issue titles (default: empty, no prefix)
- `--github-label`: Label to apply to GitHub issues (default: none)

## Output

The script creates a JSON file for each flaky test in the specified output directory. The fields returned depend on which endpoint you use:

### Using `--endpoint deprecated` (Default - Recommended)

Provides rich data about flaky test occurrences:

```json
{
  "id": "unique-test-id",
  "web_url": "https://buildkite.com/organizations/elastic/analytics/suites/beats/tests/...",
  "scope": "path.to.test.TestClass",
  "name": "test_something_important",
  "location": "src/tests/test_file.py:42",
  "file_name": "test_file.py",
  "instances": 7,
  "latest_occurrence_at": "2026-03-26T16:51:14.514Z",
  "most_recent_instance_at": "2026-03-26T16:51:14.514Z",
  "last_resolved_at": null,
  "ownership_team_ids": []
}
```

**Key fields:**
- `instances` - Number of times the test has been flaky
- `latest_occurrence_at` - When the test was last observed as flaky
- `last_resolved_at` - When the flakiness was resolved (null if still flaky)
- `ownership_team_ids` - Teams responsible for this test

### Using `--endpoint current`

Provides minimal test information:

```json
{
  "id": "unique-test-id",
  "url": "https://api.buildkite.com/v2/analytics/...",
  "web_url": "https://buildkite.com/organizations/...",
  "scope": "path.to.test.TestClass",
  "name": "test_something_important",
  "location": "src/tests/test_file.py:42",
  "file_name": "test_file.py",
  "labels": ["flaky"]
}
```

## Example

```bash
# Set up credentials
export BUILDKITE_API_TOKEN="bkua_1234567890abcdef"
export BUILDKITE_ORG_SLUG="my-company"

# Run the script for flaky tests in the last 7 days (replace with your actual suite ID)
python buildkite_flaky_report.py abc123-def456-789 --branch main --days 7

# Output:
# Connecting to Buildkite Test Engine for organization: my-company
# Fetching flaky tests from suite: abc123-def456-789
# Using endpoint: deprecated
# Branch filter: main
# Time filter: Last 7 days
#
# Found 3 flaky test(s):
# --------------------------------------------------------------------------------
#
# [1/3] Test: test_user_authentication
#   Location: tests/auth/test_auth.py:42
#   Flaky instances: 5
#   Latest occurrence: 2026-03-28T10:30:00.000Z
#   Saved to: ./flaky_tests/flaky_test_001_test_user_authentication.json
#
# [2/3] Test: test_api_timeout
#   Location: tests/api/test_timeout.py:15
#   Flaky instances: 12
#   Latest occurrence: 2026-03-27T15:45:00.000Z
#   Saved to: ./flaky_tests/flaky_test_002_test_api_timeout.json
#
# [3/3] Test: test_database_connection
#   Location: tests/db/test_connection.py:28
#   Flaky instances: 3
#   Latest occurrence: 2026-03-29T08:00:00.000Z
#   Saved to: ./flaky_tests/flaky_test_003_test_database_connection.json
#
# --------------------------------------------------------------------------------
#
# All flaky test reports saved to: ./flaky_tests
```

## Troubleshooting

### "HTTP Error: 401"
Your API token is invalid or expired. Create a new token with the correct permissions.

### "HTTP Error: 404"
The test suite ID or organization slug is incorrect. Verify:
- The suite ID from your Buildkite Test Engine URL
- The organization slug matches your Buildkite account

### "HTTP Error: 403"
Your API token doesn't have the required permissions. Make sure it has the `read_suites` and `read_test_analytics` scopes.

### No flaky tests found
This is good news! It means:
- No tests are currently labeled as "flaky" in Buildkite Test Engine
- Your tests are stable on the specified branch
- Try a different branch with `--branch` if needed

### "gh command failed" or "gh: command not found"
The GitHub CLI is not installed or not authenticated:
```bash
# Install gh CLI (macOS)
brew install gh

# Install gh CLI (Linux)
# See: https://github.com/cli/cli/blob/trunk/docs/install_linux.md

# Authenticate
gh auth login
```

### "Error creating GitHub issue: ..."
- Check that you have write permissions to the repository
- Verify the repository name is correct (`owner/repo` format)
- Ensure the `gh` CLI is properly authenticated

## GitHub Integration

The script can automatically create and manage GitHub issues for flaky tests using the `gh` CLI tool.

### Prerequisites

1. Install the GitHub CLI: [https://cli.github.com/](https://cli.github.com/)
2. Authenticate with GitHub:
   ```bash
   gh auth login
   ```

### How It Works

When you enable `--create-github-issues`, the script will:

1. **Search for existing issues** - Looks for issues with matching test name (optionally filtered by label if `--github-label` is provided)
2. **If no issue exists** - Creates a new issue with:
   - Title: `{scope} {test_name}`
   - Body: Test details, location, Buildkite link, flaky instances, timestamps
   - Label: Applied if `--github-label` is provided
3. **If closed issue exists** - Creates a new issue (test became flaky again)
4. **If open issue exists** - Adds a comment with updated information

### Issue Format

Issues are created following the format from [elastic/beats#49601](https://github.com/elastic/beats/issues/49601):

```markdown
## Flaky Test

* **Test Name:** TestFetch
* **Scope:** github.com/elastic/beats/v7/x-pack/metricbeat/module/cockroachdb/status
* **Location:** x-pack/metricbeat/module/cockroachdb/status/status_integration_test.go:37
* **Buildkite Link:** https://buildkite.com/organizations/elastic/analytics/suites/beats/tests/...
* **Flaky Instances:** 7
* **Latest Occurrence:** 2026-03-26T16:51:14.514Z

### Details
{test data JSON}
```

### Example Usage

```bash
# Detect flaky tests from last 7 days and create GitHub issues
python buildkite_flaky_report.py beats \
  --create-github-issues \
  --github-repo elastic/beats \
  --days 7
```

Output:
```
[1/3] Test: TestFetch
  Location: x-pack/metricbeat/module/cockroachdb/status/status_integration_test.go:37
  Flaky instances: 7
  Latest occurrence: 2026-03-26T16:51:14.514Z
  Saved to: ./flaky_tests/flaky_test_001_TestFetch.json
  Processing GitHub issue... Created new issue: https://github.com/elastic/beats/issues/12345
```

## Notes

- The script supports both REST API endpoints for flexibility
- Buildkite Test Engine automatically identifies and labels flaky tests
- The `--days` parameter filters tests client-side based on `latest_occurrence_at` timestamp (API doesn't support time-based filtering)
- Pagination is handled automatically to fetch all flaky tests
- The script fetches tests that are already identified as flaky by Buildkite (not analyzing test runs to determine flakiness)
- GitHub integration requires the `gh` CLI tool to be installed and authenticated
- **Note**: When using `--days`, the script fetches ALL flaky tests from the API first, then filters them locally. This ensures accurate date filtering.

## Testing

The script includes comprehensive unit tests.

### Running Tests

```bash
# Run all tests
pytest buildkite_flaky_report_tests.py -v
```

## API Documentation References

- [Buildkite Test Engine](https://buildkite.com/docs/test-engine)
- [Test Suites](https://buildkite.com/docs/test-engine/test-suites)
- [GraphQL API](https://buildkite.com/docs/apis/graphql-api)
- [REST API](https://buildkite.com/docs/apis/rest-api)
