#!/usr/bin/env python3
"""
Unit tests for buildkite_flaky_report.py

Run with: pytest buildkite_flaky_report_tests.py -v
"""

import json
import logging
import pytest
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import Mock, patch
import tempfile
import os

# Import the module to test
import buildkite_flaky_report as bft


class TestBuildkiteTestEngineClient:
    """Tests for BuildkiteTestEngineClient class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.client = bft.BuildkiteTestEngineClient("test-token", "test-org")

    def test_initialization(self):
        """Test client initialization."""
        assert self.client.api_token == "test-token"
        assert self.client.org_slug == "test-org"
        assert "Authorization" in self.client.headers
        assert self.client.headers["Authorization"] == "Bearer test-token"

    @patch('requests.get')
    def test_make_request_success(self, mock_get):
        """Test successful API request."""
        mock_response = Mock()
        mock_response.json.return_value = {"test": "data"}
        mock_get.return_value = mock_response

        result = self.client._make_request("/test/endpoint", {"param": "value"})

        assert result == {"test": "data"}
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert "/test/endpoint" in args[0]
        assert kwargs["params"] == {"param": "value"}

    @patch('requests.get')
    def test_make_request_failure(self, mock_get):
        """Test API request failure."""
        mock_get.side_effect = Exception("API Error")

        with pytest.raises(Exception):
            self.client._make_request("/test/endpoint")

    def test_parse_iso_timestamp(self):
        """Test ISO timestamp parsing."""
        timestamp = "2026-03-30T10:30:00.000Z"
        result = bft.BuildkiteTestEngineClient._parse_iso_timestamp(timestamp)

        assert result.year == 2026
        assert result.month == 3
        assert result.day == 30

    @patch.object(bft.BuildkiteTestEngineClient, '_make_request')
    def test_get_flaky_tests_deprecated_endpoint(self, mock_request):
        """Test get_flaky_tests with deprecated endpoint."""
        mock_request.return_value = [
            {"id": "1", "name": "test1"},
            {"id": "2", "name": "test2"}
        ]

        result = self.client.get_flaky_tests(
            "suite-id",
            branch="main",
            per_page=100,
            days=None,
            use_deprecated_endpoint=True
        )

        assert len(result) == 2
        mock_request.assert_called_once()
        args = mock_request.call_args[0]
        assert "flaky-tests" in args[0]

    @patch.object(bft.BuildkiteTestEngineClient, '_make_request')
    def test_get_flaky_tests_current_endpoint(self, mock_request):
        """Test get_flaky_tests with current endpoint."""
        mock_request.return_value = [
            {"id": "1", "name": "test1", "labels": ["flaky"]}
        ]

        result = self.client.get_flaky_tests(
            "suite-id",
            use_deprecated_endpoint=False
        )

        assert len(result) == 1
        # Check the endpoint URL (first positional arg)
        endpoint = mock_request.call_args[0][0]
        assert "flaky-tests" not in endpoint
        # Check the params dict (second positional arg)
        params = mock_request.call_args[0][1]
        assert params["label"] == "flaky"

    @patch.object(bft.BuildkiteTestEngineClient, '_make_request')
    def test_get_flaky_tests_with_branch_filter(self, mock_request):
        """Test get_flaky_tests with branch filter."""
        mock_request.return_value = []

        self.client.get_flaky_tests("suite-id", branch="develop")

        # Check the params dict (second positional arg to _make_request)
        params = mock_request.call_args[0][1]
        assert params["branch"] == "develop"

    @patch.object(bft.BuildkiteTestEngineClient, '_make_request')
    def test_get_flaky_tests_with_date_filter(self, mock_request):
        """Test get_flaky_tests with date filtering."""
        now = datetime.now(timezone.utc)
        old_date = (now - timedelta(days=10)).isoformat()
        recent_date = (now - timedelta(days=2)).isoformat()

        mock_request.return_value = [
            {"id": "1", "name": "old_test", "latest_occurrence_at": old_date},
            {"id": "2", "name": "recent_test", "latest_occurrence_at": recent_date},
            {"id": "3", "name": "no_date_test"}
        ]

        result = self.client.get_flaky_tests(
            "suite-id",
            days=7,
            use_deprecated_endpoint=True
        )

        # Should filter out old_test but keep recent_test and no_date_test
        assert len(result) == 2
        assert result[0]["name"] == "recent_test"
        assert result[1]["name"] == "no_date_test"

    @patch.object(bft.BuildkiteTestEngineClient, '_make_request')
    def test_get_flaky_tests_date_filter_with_current_endpoint(self, mock_request, caplog):
        """Test that date filtering warns with current endpoint."""
        mock_request.return_value = [
            {"id": "1", "name": "test1", "labels": ["flaky"]}
        ]

        with caplog.at_level(logging.WARNING, logger='buildkite_flaky_report'):
            result = self.client.get_flaky_tests(
                "suite-id",
                days=7,
                use_deprecated_endpoint=False
            )

        # Should return all tests with a warning
        assert len(result) == 1
        assert "Cannot filter by days" in caplog.text

    @patch.object(bft.BuildkiteTestEngineClient, '_make_request')
    def test_get_flaky_tests_pagination(self, mock_request):
        """Test pagination handling."""
        # First page returns full page, second page returns partial
        mock_request.side_effect = [
            [{"id": str(i)} for i in range(100)],  # Full page
            [{"id": "100"}]  # Partial page (last page)
        ]

        result = self.client.get_flaky_tests("suite-id", per_page=100)

        assert len(result) == 101
        assert mock_request.call_count == 2

    @patch.object(bft.BuildkiteTestEngineClient, '_make_request')
    @patch.object(bft.BuildkiteTestEngineClient, '_filter_by_days')
    def test_get_flaky_tests_with_days_zero(self, mock_filter, mock_request):
        """Test get_flaky_tests with days=0 calls filter (not treated as falsy)."""
        mock_request.return_value = [
            {"id": "1", "name": "test1"},
            {"id": "2", "name": "test2"},
        ]
        mock_filter.return_value = [{"id": "1", "name": "test1"}]

        self.client.get_flaky_tests(
            "suite-id",
            days=0,
            use_deprecated_endpoint=True
        )

        # The key test: _filter_by_days should be called even when days=0
        # (Previously it wasn't called because "if days" treated 0 as falsy)
        mock_filter.assert_called_once()
        call_args = mock_filter.call_args[0]
        assert call_args[1] == 0  # days parameter should be 0

    @patch.object(bft.BuildkiteTestEngineClient, '_make_request')
    @patch.object(bft.BuildkiteTestEngineClient, '_filter_by_days')
    def test_get_flaky_tests_with_days_none_skips_filter(self, mock_filter, mock_request):
        """Test get_flaky_tests with days=None skips filtering."""
        mock_request.return_value = [
            {"id": "1", "name": "test1"},
            {"id": "2", "name": "test2"},
        ]

        self.client.get_flaky_tests(
            "suite-id",
            days=None,
            use_deprecated_endpoint=True
        )

        # _filter_by_days should NOT be called when days=None
        mock_filter.assert_not_called()


class TestGitHubIssueManager:
    """Tests for GitHubIssueManager class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.manager = bft.GitHubIssueManager("test-org/test-repo")

    def test_initialization(self):
        """Test GitHub manager initialization with defaults."""
        assert self.manager.repo == "test-org/test-repo"
        assert self.manager.issue_title_prefix == ""
        assert self.manager.github_label is None

    def test_initialization_with_custom_settings(self):
        """Test GitHub manager initialization with custom settings."""
        manager = bft.GitHubIssueManager(
            "test-org/test-repo",
            issue_title_prefix="[FLAKY]",
            github_label="custom-label"
        )
        assert manager.issue_title_prefix == "[FLAKY]"
        assert manager.github_label == "custom-label"

    def test_format_issue_title_with_prefix(self):
        """Test issue title formatting with prefix."""
        manager = bft.GitHubIssueManager("test-org/test-repo", issue_title_prefix="[Flaky Test]")
        title = manager._format_issue_title("TestFoo", "my.scope")
        assert title == "[Flaky Test] my.scope TestFoo"

    def test_format_issue_title_without_prefix(self):
        """Test issue title formatting without prefix (default)."""
        title = self.manager._format_issue_title("TestBar", "another.scope")
        assert title == "another.scope TestBar"

    @patch('subprocess.run')
    def test_run_gh_command_success(self, mock_run):
        """Test successful gh command execution."""
        mock_run.return_value = Mock(stdout="command output\n", returncode=0)

        result = self.manager._run_gh_command(["issue", "list"])

        assert result == "command output"
        mock_run.assert_called_once()

    @patch('subprocess.run')
    def test_run_gh_command_failure(self, mock_run):
        """Test gh command failure."""
        mock_run.side_effect = subprocess.CalledProcessError(1, "gh", stderr="error")

        with pytest.raises(subprocess.CalledProcessError):
            self.manager._run_gh_command(["issue", "list"])

    @patch.object(bft.GitHubIssueManager, '_run_gh_command')
    def test_search_existing_issue_found(self, mock_gh):
        """Test searching for existing issue - found."""
        mock_gh.return_value = json.dumps([
            {
                "number": 123,
                "title": "[Flaky Test] my.scope TestFoo",
                "state": "OPEN",
                "url": "https://github.com/test-org/test-repo/issues/123"
            }
        ])

        result = self.manager.search_existing_issue("TestFoo", "my.scope")

        assert result is not None
        assert result["number"] == 123
        assert result["state"] == "OPEN"

    @patch.object(bft.GitHubIssueManager, '_run_gh_command')
    def test_search_existing_issue_not_found(self, mock_gh):
        """Test searching for existing issue - not found."""
        mock_gh.return_value = json.dumps([])

        result = self.manager.search_existing_issue("TestBar", "my.scope")

        assert result is None

    @patch.object(bft.GitHubIssueManager, '_run_gh_command')
    def test_create_issue_success(self, mock_gh):
        """Test creating a new GitHub issue."""
        mock_gh.return_value = "https://github.com/test-org/test-repo/issues/456"

        test_data = {
            "name": "TestFoo",
            "scope": "my.scope",
            "location": "test.py:42",
            "web_url": "https://buildkite.com/test",
            "instances": 5,
            "latest_occurrence_at": "2026-03-29T10:00:00Z"
        }

        result = self.manager.create_issue(test_data)

        assert result == "https://github.com/test-org/test-repo/issues/456"
        mock_gh.assert_called_once()
        args = mock_gh.call_args[0][0]
        assert "issue" in args
        assert "create" in args

    @patch.object(bft.GitHubIssueManager, '_run_gh_command')
    def test_add_comment_success(self, mock_gh):
        """Test adding a comment to existing issue."""
        mock_gh.return_value = ""

        test_data = {
            "name": "TestFoo",
            "web_url": "https://buildkite.com/test",
            "latest_occurrence_at": "2026-03-29T10:00:00Z",
            "instances": 7
        }

        result = self.manager.add_comment(123, test_data)

        assert result is True
        mock_gh.assert_called_once()
        args = mock_gh.call_args[0][0]
        assert "comment" in args
        assert "123" in args

    @patch.object(bft.GitHubIssueManager, '_run_gh_command')
    def test_add_comment_with_failure_examples(self, mock_gh):
        """Test adding a comment includes recent failure examples."""
        mock_gh.return_value = ""

        test_data = {
            "name": "TestFoo",
            "web_url": "https://buildkite.com/test",
            "latest_occurrence_at": "2026-03-29T10:00:00Z",
            "instances": 7,
            "failure_examples": [
                {
                    "message": ["Error line 1", "Error line 2"],
                    "run_url": "http://example.com/run/1",
                    "run_time": "2026-03-29T10:00:00Z"
                }
            ]
        }

        result = self.manager.add_comment(123, test_data)

        assert result is True
        mock_gh.assert_called_once()
        args = mock_gh.call_args[0][0]
        body_index = args.index("--body") + 1
        body = args[body_index]

        # Should include failure examples in comment
        assert "Failure Examples" in body
        assert "Error line 1" in body

    @patch.object(bft.GitHubIssueManager, 'search_existing_issue')
    @patch.object(bft.GitHubIssueManager, 'create_issue')
    def test_process_flaky_test_no_existing_issue(self, mock_create, mock_search):
        """Test processing flaky test - no existing issue."""
        mock_search.return_value = None
        mock_create.return_value = "https://github.com/test-org/test-repo/issues/789"

        test_data = {"name": "TestNew", "scope": "scope"}
        status, was_created = self.manager.process_flaky_test(test_data)

        assert was_created is True
        assert "Created new issue" in status
        mock_create.assert_called_once()

    @patch.object(bft.GitHubIssueManager, 'search_existing_issue')
    @patch.object(bft.GitHubIssueManager, 'create_issue')
    def test_process_flaky_test_closed_issue_exists(self, mock_create, mock_search):
        """Test processing flaky test - closed issue exists."""
        mock_search.return_value = {
            "number": 100,
            "state": "CLOSED",
            "url": "https://github.com/test-org/test-repo/issues/100"
        }
        mock_create.return_value = "https://github.com/test-org/test-repo/issues/200"

        test_data = {"name": "TestOld", "scope": "scope"}
        status, was_created = self.manager.process_flaky_test(test_data)

        assert was_created is True
        assert "Created new issue" in status
        assert "#100" in status
        mock_create.assert_called_once()

    @patch.object(bft.GitHubIssueManager, 'search_existing_issue')
    @patch.object(bft.GitHubIssueManager, 'add_comment')
    def test_process_flaky_test_open_issue_exists(self, mock_comment, mock_search):
        """Test processing flaky test - open issue exists."""
        mock_search.return_value = {
            "number": 100,
            "state": "OPEN",
            "url": "https://github.com/test-org/test-repo/issues/100"
        }
        mock_comment.return_value = True

        test_data = {"name": "TestExisting", "scope": "scope"}
        status, was_created = self.manager.process_flaky_test(test_data)

        assert was_created is False
        assert "Added comment" in status
        assert "#100" in status
        mock_comment.assert_called_once()


class TestMaxIssuesLimit:
    """Tests for max-issues limit functionality."""

    @patch.object(bft.BuildkiteTestEngineClient, 'get_flaky_tests')
    @patch.object(bft.GitHubIssueManager, 'process_flaky_test')
    def test_max_issues_zero_creates_no_issues(self, mock_process, mock_get_tests):
        """Test that max-issues=0 creates no GitHub issues but still writes JSON files."""
        # Return some flaky tests
        mock_get_tests.return_value = [
            {"name": "Test1", "scope": "scope1", "location": "test1.py:1"},
            {"name": "Test2", "scope": "scope2", "location": "test2.py:2"}
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('sys.argv', [
                'buildkite_flaky_report.py', 'test-suite-id',
                '--org', 'test-org', '--api-token', 'test-token',
                '--create-github-issues', '--github-repo', 'test/repo',
                '--max-issues', '0', '--output-dir', tmpdir
            ]):
                bft.main()

            # process_flaky_test should never be called because max-issues is 0
            mock_process.assert_not_called()

            # But JSON files should still be written for all tests
            json_files = list(Path(tmpdir).glob("*.json"))
            assert len(json_files) == 2

    @patch.object(bft.BuildkiteTestEngineClient, 'get_flaky_tests')
    @patch.object(bft.GitHubIssueManager, 'process_flaky_test')
    def test_max_issues_limit_enforced(self, mock_process, mock_get_tests):
        """Test that max-issues limits GitHub issue creation but processes all tests."""
        # Return multiple flaky tests
        mock_get_tests.return_value = [
            {"name": "Test1", "scope": "scope1", "location": "test1.py:1"},
            {"name": "Test2", "scope": "scope2", "location": "test2.py:2"},
            {"name": "Test3", "scope": "scope3", "location": "test3.py:3"},
        ]
        # Each call creates a new issue
        mock_process.return_value = ("Created new issue", True)

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('sys.argv', [
                'buildkite_flaky_report.py', 'test-suite-id',
                '--org', 'test-org', '--api-token', 'test-token',
                '--create-github-issues', '--github-repo', 'test/repo',
                '--max-issues', '2', '--output-dir', tmpdir
            ]):
                bft.main()

            # Should only create 2 GitHub issues (the limit)
            assert mock_process.call_count == 2

            # But should still write JSON files for all 3 tests
            json_files = list(Path(tmpdir).glob("*.json"))
            assert len(json_files) == 3

    @patch.object(bft.BuildkiteTestEngineClient, 'get_flaky_tests')
    @patch.object(bft.GitHubIssueManager, 'process_flaky_test')
    def test_max_issues_mixed_creates_and_updates(self, mock_process, mock_get_tests):
        """Test max-issues counts only new issues created, not updates."""
        # Return multiple flaky tests
        mock_get_tests.return_value = [
            {"name": "Test1", "scope": "scope1", "location": "test1.py:1"},
            {"name": "Test2", "scope": "scope2", "location": "test2.py:2"},
            {"name": "Test3", "scope": "scope3", "location": "test3.py:3"},
            {"name": "Test4", "scope": "scope4", "location": "test4.py:4"},
        ]
        # First creates new issue, second updates existing, third creates new, fourth would be skipped
        mock_process.side_effect = [
            ("Created new issue", True),
            ("Added comment to existing issue", False),
            ("Created new issue", True),
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('sys.argv', [
                'buildkite_flaky_report.py', 'test-suite-id',
                '--org', 'test-org', '--api-token', 'test-token',
                '--create-github-issues', '--github-repo', 'test/repo',
                '--max-issues', '2', '--output-dir', tmpdir
            ]):
                bft.main()

            # First creates (count=1), second updates (count=1), third creates (count=2), fourth skipped
            assert mock_process.call_count == 3

            # All 4 tests should have JSON files
            json_files = list(Path(tmpdir).glob("*.json"))
            assert len(json_files) == 4

    @patch.object(bft.BuildkiteTestEngineClient, 'get_flaky_tests')
    @patch.object(bft.GitHubIssueManager, 'process_flaky_test')
    def test_max_issues_limit_on_first_test(self, mock_process, mock_get_tests, caplog):
        """Test max-issues=1 stops issue creation after first test."""
        mock_get_tests.return_value = [
            {"name": "Test1", "scope": "scope1", "location": "test1.py:1"},
            {"name": "Test2", "scope": "scope2", "location": "test2.py:2"},
        ]
        mock_process.return_value = ("Created new issue", True)

        with tempfile.TemporaryDirectory() as tmpdir:
            with caplog.at_level(logging.INFO, logger='buildkite_flaky_report'):
                with patch('sys.argv', [
                    'buildkite_flaky_report.py', 'test-suite-id',
                    '--org', 'test-org', '--api-token', 'test-token',
                    '--create-github-issues', '--github-repo', 'test/repo',
                    '--max-issues', '1', '--output-dir', tmpdir
                ]):
                    bft.main()

            # Only first test should create issue
            assert mock_process.call_count == 1

            # Both tests should have JSON files
            json_files = list(Path(tmpdir).glob("*.json"))
            assert len(json_files) == 2

            # Verify skip message was logged
            assert 'Skipping GitHub issue' in caplog.text

    @patch.object(bft.BuildkiteTestEngineClient, 'get_flaky_tests')
    @patch.object(bft.GitHubIssueManager, 'process_flaky_test')
    def test_max_issues_summary_output(self, mock_process, mock_get_tests, caplog):
        """Test that summary correctly shows skipped count."""
        mock_get_tests.return_value = [
            {"name": "Test1", "scope": "scope1", "location": "test1.py:1"},
            {"name": "Test2", "scope": "scope2", "location": "test2.py:2"},
            {"name": "Test3", "scope": "scope3", "location": "test3.py:3"},
        ]
        mock_process.return_value = ("Created new issue", True)

        with tempfile.TemporaryDirectory() as tmpdir:
            with caplog.at_level(logging.INFO, logger='buildkite_flaky_report'):
                with patch('sys.argv', [
                    'buildkite_flaky_report.py', 'test-suite-id',
                    '--org', 'test-org', '--api-token', 'test-token',
                    '--create-github-issues', '--github-repo', 'test/repo',
                    '--max-issues', '1', '--output-dir', tmpdir
                ]):
                    bft.main()

            # Check summary output
            assert 'New issues created: 1' in caplog.text
            assert 'Issue creation limit: 1' in caplog.text
            assert 'Tests skipped (limit reached): 2' in caplog.text

    @patch.object(bft.BuildkiteTestEngineClient, 'get_flaky_tests')
    def test_no_github_manager_processes_all_tests(self, mock_get_tests):
        """Test that without GitHub manager, all tests are processed."""
        mock_get_tests.return_value = [
            {"name": "Test1", "scope": "scope1", "location": "test1.py:1"},
            {"name": "Test2", "scope": "scope2", "location": "test2.py:2"},
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('sys.argv', [
                'buildkite_flaky_report.py', 'test-suite-id',
                '--org', 'test-org', '--api-token', 'test-token',
                '--output-dir', tmpdir
            ]):
                bft.main()

            # Both tests should have JSON files
            json_files = list(Path(tmpdir).glob("*.json"))
            assert len(json_files) == 2


class TestHelperFunctions:
    """Tests for helper functions."""

    def test_save_flaky_test_to_file(self):
        """Test saving flaky test data to file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            test_data = {
                "id": "test-123",
                "name": "TestFoo",
                "identifier": "my.package.TestFoo",
                "location": "test.py:42"
            }

            filepath = bft.save_flaky_test_to_file(test_data, output_dir, 1)

            assert os.path.exists(filepath)
            assert "flaky_test_001" in filepath
            assert "TestFoo" in filepath

            # Verify content
            with open(filepath, 'r') as f:
                saved_data = json.load(f)
            assert saved_data == test_data

    def test_save_flaky_test_to_file_with_special_chars(self):
        """Test saving with special characters in test name."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            test_data = {
                "name": "Test/With\\Special:Chars",
                "id": "123"
            }

            filepath = bft.save_flaky_test_to_file(test_data, output_dir, 5)

            assert os.path.exists(filepath)
            assert "flaky_test_005" in filepath
            # Special chars should be replaced with underscores
            assert "/" not in os.path.basename(filepath)
            assert "\\" not in os.path.basename(filepath)

    def test_save_flaky_test_creates_directory(self):
        """Test that save_flaky_test_to_file creates output directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "new_dir" / "nested"
            test_data = {"name": "Test", "id": "1"}

            filepath = bft.save_flaky_test_to_file(test_data, output_dir, 1)

            assert os.path.exists(filepath)
            assert os.path.exists(output_dir)


class TestDateFiltering:
    """Tests for date filtering logic."""

    def test_date_parsing_iso_format(self):
        """Test parsing ISO 8601 dates."""
        date_str = "2026-03-29T10:30:00.000Z"
        parsed = datetime.fromisoformat(date_str.replace('Z', '+00:00'))

        assert parsed.year == 2026
        assert parsed.month == 3
        assert parsed.day == 29

    def test_date_comparison(self):
        """Test date comparison for filtering."""
        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(days=7)

        recent = now - timedelta(days=2)
        old = now - timedelta(days=10)

        assert recent >= cutoff
        assert old < cutoff

    @patch.object(bft.BuildkiteTestEngineClient, '_make_request')
    def test_filter_preserves_tests_without_dates(self, mock_request):
        """Test that tests without dates are preserved during filtering."""
        client = bft.BuildkiteTestEngineClient("token", "org")

        mock_request.return_value = [
            {"id": "1", "name": "test_no_date"},
            {"id": "2", "name": "test_null_date", "latest_occurrence_at": None}
        ]

        result = client.get_flaky_tests(
            "suite-id",
            days=7,
            use_deprecated_endpoint=True
        )

        # Both tests should be included
        assert len(result) == 2

    @patch.object(bft.BuildkiteTestEngineClient, '_make_request')
    def test_filter_by_days_actual_filtering(self, mock_request):
        """Test actual date filtering with different timestamps."""
        client = bft.BuildkiteTestEngineClient("token", "org")
        now = datetime.now(timezone.utc)

        # Create tests with various ages
        tests = [
            {"id": "1", "name": "very_old", "latest_occurrence_at": (now - timedelta(days=30)).isoformat()},
            {"id": "2", "name": "old", "latest_occurrence_at": (now - timedelta(days=10)).isoformat()},
            {"id": "3", "name": "recent", "latest_occurrence_at": (now - timedelta(days=3)).isoformat()},
            {"id": "4", "name": "today", "latest_occurrence_at": (now - timedelta(hours=2)).isoformat()},
        ]

        mock_request.return_value = tests

        # Filter to last 7 days
        result = client.get_flaky_tests("suite-id", days=7, use_deprecated_endpoint=True)

        # Should only get tests from last 7 days (recent and today)
        assert len(result) == 2
        names = [t["name"] for t in result]
        assert "recent" in names
        assert "today" in names
        assert "old" not in names
        assert "very_old" not in names

    @patch.object(bft.BuildkiteTestEngineClient, '_make_request')
    def test_filter_with_invalid_date_format(self, mock_request):
        """Test that invalid date formats are handled gracefully."""
        client = bft.BuildkiteTestEngineClient("token", "org")
        now = datetime.now(timezone.utc)

        tests = [
            {"id": "1", "name": "invalid_date", "latest_occurrence_at": "not-a-date"},
            {"id": "2", "name": "valid_date", "latest_occurrence_at": (now - timedelta(days=1)).isoformat()},
        ]

        mock_request.return_value = tests

        # Should not crash, should include test with invalid date
        result = client.get_flaky_tests("suite-id", days=7, use_deprecated_endpoint=True)

        assert len(result) == 2  # Both included (invalid dates are preserved)

    @patch.object(bft.BuildkiteTestEngineClient, 'get_flaky_tests')
    def test_days_zero_message_output(self, mock_get_tests, caplog):
        """Test that days=0 shows correct message in output."""
        mock_get_tests.return_value = []

        with tempfile.TemporaryDirectory() as tmpdir:
            with caplog.at_level(logging.INFO, logger='buildkite_flaky_report'):
                with patch('sys.argv', [
                    'buildkite_flaky_report.py', 'test-suite-id',
                    '--org', 'test-org', '--api-token', 'test-token',
                    '--days', '0', '--output-dir', tmpdir
                ]):
                    bft.main()

            # Check that "Last 0 days" appears in output
            assert 'Last 0 days' in caplog.text

    @patch.object(bft.BuildkiteTestEngineClient, 'get_flaky_tests')
    def test_days_default_shows_time_filter(self, mock_get_tests, caplog):
        """Test that default days value (1) shows time filter message."""
        mock_get_tests.return_value = []

        with tempfile.TemporaryDirectory() as tmpdir:
            with caplog.at_level(logging.INFO, logger='buildkite_flaky_report'):
                with patch('sys.argv', [
                    'buildkite_flaky_report.py', 'test-suite-id',
                    '--org', 'test-org', '--api-token', 'test-token',
                    '--output-dir', tmpdir
                ]):
                    bft.main()

            # Default days=1 should show "Time filter: Last 1 days"
            assert 'Time filter: Last 1 days' in caplog.text


class TestCLIValidation:
    """Tests for CLI argument validation."""

    def test_negative_days_validation(self, caplog):
        """Test that negative days value is rejected."""
        with caplog.at_level(logging.ERROR, logger='buildkite_flaky_report'):
            with patch('sys.argv', ['buildkite_flaky_report.py', 'test-suite-id', '--org', 'test-org', '--api-token', 'test-token', '--days', '-1']):
                with pytest.raises(SystemExit) as exc_info:
                    bft.main()

        assert exc_info.value.code == 1
        assert '--days must be >= 0' in caplog.text

    def test_negative_max_issues_validation(self, caplog):
        """Test that negative max-issues value is rejected."""
        with caplog.at_level(logging.ERROR, logger='buildkite_flaky_report'):
            with patch('sys.argv', ['buildkite_flaky_report.py', 'test-suite-id', '--org', 'test-org', '--api-token', 'test-token', '--max-issues', '-5']):
                with pytest.raises(SystemExit) as exc_info:
                    bft.main()

        assert exc_info.value.code == 1
        assert '--max-issues must be >= 0' in caplog.text

    def test_days_zero_is_valid(self):
        """Test that days=0 is accepted (not treated as falsy)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('sys.argv', ['buildkite_flaky_report.py', 'test-suite-id', '--org', 'test-org', '--api-token', 'test-token', '--days', '0', '--output-dir', tmpdir]):
                with patch.object(bft.BuildkiteTestEngineClient, 'get_flaky_tests', return_value=[]):
                    # Should not raise SystemExit - if it completes, days=0 was accepted
                    bft.main()

    def test_missing_api_token_exits(self, caplog):
        """Test that missing API token exits with an error."""
        with caplog.at_level(logging.ERROR, logger='buildkite_flaky_report'):
            with patch('sys.argv', ['buildkite_flaky_report.py', 'test-suite-id', '--org', 'test-org']):
                with patch.dict(os.environ, {}, clear=True):
                    with pytest.raises(SystemExit) as exc_info:
                        bft.main()

        assert exc_info.value.code == 1
        assert 'API token is required' in caplog.text

    def test_missing_org_exits(self, caplog):
        """Test that missing organization slug exits with an error."""
        with caplog.at_level(logging.ERROR, logger='buildkite_flaky_report'):
            with patch('sys.argv', ['buildkite_flaky_report.py', 'test-suite-id', '--api-token', 'test-token']):
                with patch.dict(os.environ, {}, clear=True):
                    with pytest.raises(SystemExit) as exc_info:
                        bft.main()

        assert exc_info.value.code == 1
        assert 'Organization slug is required' in caplog.text

    def test_missing_github_repo_with_create_issues_exits(self, caplog):
        """Test that --create-github-issues without --github-repo exits with an error."""
        with caplog.at_level(logging.ERROR, logger='buildkite_flaky_report'):
            with patch('sys.argv', [
                'buildkite_flaky_report.py', 'test-suite-id',
                '--org', 'test-org', '--api-token', 'test-token',
                '--create-github-issues'
            ]):
                with pytest.raises(SystemExit) as exc_info:
                    bft.main()

        assert exc_info.value.code == 1
        assert '--github-repo is required' in caplog.text


class TestOutputValidation:
    """Tests for output count and file generation."""

    @patch.object(bft.BuildkiteTestEngineClient, 'get_flaky_tests')
    def test_output_count_matches_detected_tests(self, mock_get_tests, caplog):
        """Test that output count reflects all detected tests, not just issues created."""
        mock_get_tests.return_value = [
            {"name": "Test1", "scope": "scope1", "location": "test1.py:1"},
            {"name": "Test2", "scope": "scope2", "location": "test2.py:2"},
            {"name": "Test3", "scope": "scope3", "location": "test3.py:3"},
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            with caplog.at_level(logging.INFO, logger='buildkite_flaky_report'):
                with patch('sys.argv', [
                    'buildkite_flaky_report.py', 'test-suite-id',
                    '--org', 'test-org', '--api-token', 'test-token',
                    '--output-dir', tmpdir
                ]):
                    bft.main()

            # Should have 3 JSON files
            json_files = list(Path(tmpdir).glob("*.json"))
            assert len(json_files) == 3

            # Output should mention 3 tests found
            assert 'Found 3 flaky test' in caplog.text

class TestEdgeCases:
    """Tests for edge cases and error handling."""

    @patch.object(bft.BuildkiteTestEngineClient, '_make_request')
    def test_empty_response(self, mock_request):
        """Test handling empty API response."""
        mock_request.return_value = []

        client = bft.BuildkiteTestEngineClient("token", "org")
        result = client.get_flaky_tests("suite-id")

        assert result == []

    @patch.object(bft.GitHubIssueManager, '_run_gh_command')
    def test_github_search_with_error(self, mock_gh):
        """Test GitHub search handling errors gracefully."""
        mock_gh.side_effect = Exception("Network error")

        manager = bft.GitHubIssueManager("org/repo")
        result = manager.search_existing_issue("Test", "scope")

        # Should return None instead of crashing
        assert result is None

    def test_save_with_very_long_filename(self):
        """Test saving with very long test identifier."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            test_data = {
                "identifier": "a" * 500,  # Very long name
                "name": "Test",
                "id": "1"
            }

            filepath = bft.save_flaky_test_to_file(test_data, output_dir, 1)

            # Should truncate to reasonable length
            filename = os.path.basename(filepath)
            assert len(filename) < 250
            assert os.path.exists(filepath)

    @patch.object(bft.BuildkiteTestEngineClient, 'get_flaky_tests')
    @patch.object(bft.GitHubIssueManager, 'process_flaky_test')
    def test_all_updates_no_creates_with_max_issues(self, mock_process, mock_get_tests):
        """Test that max-issues doesn't apply when all tests update existing issues."""
        mock_get_tests.return_value = [
            {"name": "Test1", "scope": "scope1", "location": "test1.py:1"},
            {"name": "Test2", "scope": "scope2", "location": "test2.py:2"},
            {"name": "Test3", "scope": "scope3", "location": "test3.py:3"},
        ]
        # All tests update existing issues (was_created=False)
        mock_process.return_value = ("Added comment", False)

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('sys.argv', [
                'buildkite_flaky_report.py', 'test-suite-id',
                '--org', 'test-org', '--api-token', 'test-token',
                '--create-github-issues', '--github-repo', 'test/repo',
                '--max-issues', '1', '--output-dir', tmpdir
            ]):
                bft.main()

            # All 3 should be processed since none create new issues
            assert mock_process.call_count == 3

    @patch.object(bft.BuildkiteTestEngineClient, 'get_flaky_tests')
    def test_deprecated_endpoint_with_instances(self, mock_get_tests, caplog):
        """Test that deprecated endpoint shows instance info."""
        mock_get_tests.return_value = [
            {
                "name": "Test1",
                "scope": "scope1",
                "location": "test1.py:1",
                "instances": 5,
                "latest_occurrence_at": "2026-03-30T10:00:00Z",
                "last_resolved_at": "2026-03-29T10:00:00Z"
            }
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            with caplog.at_level(logging.INFO, logger='buildkite_flaky_report'):
                with patch('sys.argv', [
                    'buildkite_flaky_report.py', 'test-suite-id',
                    '--org', 'test-org', '--api-token', 'test-token',
                    '--endpoint', 'deprecated', '--output-dir', tmpdir
                ]):
                    bft.main()

            # Check that instance info is logged
            assert 'Flaky instances: 5' in caplog.text
            assert 'Latest occurrence' in caplog.text
            assert 'Last resolved' in caplog.text

    @patch.object(bft.BuildkiteTestEngineClient, 'get_flaky_tests')
    def test_current_endpoint_no_instances(self, mock_get_tests, caplog):
        """Test that current endpoint doesn't show instance info."""
        mock_get_tests.return_value = [
            {"name": "Test1", "scope": "scope1", "location": "test1.py:1"}
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            with caplog.at_level(logging.INFO, logger='buildkite_flaky_report'):
                with patch('sys.argv', [
                    'buildkite_flaky_report.py', 'test-suite-id',
                    '--org', 'test-org', '--api-token', 'test-token',
                    '--endpoint', 'current', '--output-dir', tmpdir
                ]):
                    bft.main()

            # Instance info should not be logged
            assert 'Flaky instances' not in caplog.text


class TestFailureEnrichment:
    """Tests for failure enrichment functionality."""

    def setup_method(self):
        """Set up test fixtures."""
        self.client = bft.BuildkiteTestEngineClient("test-token", "test-org")

    @patch.object(bft.BuildkiteTestEngineClient, '_make_request')
    def test_get_recent_runs(self, mock_request):
        """Test fetching recent runs."""
        mock_request.return_value = [
            {"id": "run-1", "url": "https://example.com/run-1", "created_at": "2026-03-31T10:00:00Z"},
            {"id": "run-2", "url": "https://example.com/run-2", "created_at": "2026-03-31T09:00:00Z"}
        ]

        result = self.client.get_recent_runs("suite-id", limit=50)

        assert len(result) == 2
        assert result[0]["id"] == "run-1"
        mock_request.assert_called_once()
        args = mock_request.call_args[0]
        assert "runs" in args[0]

    @patch.object(bft.BuildkiteTestEngineClient, '_make_request')
    def test_get_failed_executions(self, mock_request):
        """Test fetching failed executions for a run."""
        mock_request.return_value = [
            {
                "test_id": "test-123",
                "failure_reason": "AssertionError: test failed"
            }
        ]

        result = self.client.get_failed_executions("suite-id", "run-1")

        assert len(result) == 1
        assert result[0]["test_id"] == "test-123"
        mock_request.assert_called_once()
        args = mock_request.call_args[0]
        assert "failed_executions" in args[0]
        assert "run-1" in args[0]
        # Check that include_failure_expanded parameter is passed
        params = mock_request.call_args[0][1]
        assert params["include_failure_expanded"] == "true"

    @patch.object(bft.BuildkiteTestEngineClient, '_make_request')
    def test_get_failed_executions_error_handling(self, mock_request):
        """Test failed executions handles errors gracefully."""
        mock_request.side_effect = Exception("API Error")

        result = self.client.get_failed_executions("suite-id", "run-1")

        assert result == []

    @patch.object(bft.BuildkiteTestEngineClient, 'get_recent_runs')
    @patch.object(bft.BuildkiteTestEngineClient, 'get_failed_executions')
    def test_enrich_flaky_tests_with_failures(self, mock_get_executions, mock_get_runs):
        """Test enriching flaky tests with failure details."""
        # Setup mock data
        mock_get_runs.return_value = [
            {
                "id": "run-1",
                "url": "https://example.com/run-1",
                "created_at": "2026-03-31T10:00:00Z"
            }
        ]

        mock_get_executions.return_value = [
            {
                "test_id": "test-123",
                "failure_reason": "AssertionError: Expected 5 but got 4"
            }
        ]

        flaky_tests = [
            {
                "id": "test-123",
                "name": "test_foo",
                "scope": "module.Test"
            }
        ]

        result = self.client.enrich_flaky_tests_with_failures("suite-id", flaky_tests)

        assert len(result) == 1
        assert "failure_examples" in result[0]
        assert len(result[0]["failure_examples"]) == 1

        # Check structure of failure example
        failure = result[0]["failure_examples"][0]
        assert isinstance(failure, dict)
        assert "message" in failure
        assert "run_url" in failure
        assert "run_time" in failure
        # Message should be a list of strings
        assert isinstance(failure["message"], list)
        assert "AssertionError: Expected 5 but got 4" in failure["message"]
        assert failure["run_url"] == "https://example.com/run-1"

    @patch.object(bft.BuildkiteTestEngineClient, 'get_recent_runs')
    @patch.object(bft.BuildkiteTestEngineClient, 'get_failed_executions')
    def test_enrich_flaky_tests_deduplication(self, mock_get_executions, mock_get_runs):
        """Test that duplicate failures are not added."""
        # Setup mock data with duplicate failures
        mock_get_runs.return_value = [
            {"id": "run-1", "url": "https://example.com/run-1", "created_at": "2026-03-31T10:00:00Z"},
            {"id": "run-2", "url": "https://example.com/run-2", "created_at": "2026-03-31T09:00:00Z"}
        ]

        # Both runs return the same failure
        mock_get_executions.side_effect = [
            [{"test_id": "test-123", "failure_reason": "Same error"}],
            [{"test_id": "test-123", "failure_reason": "Same error"}]
        ]

        flaky_tests = [{"id": "test-123", "name": "test_foo"}]

        result = self.client.enrich_flaky_tests_with_failures("suite-id", flaky_tests)

        # Should only have one failure example despite two runs with same error
        assert len(result[0]["failure_examples"]) == 1

    @patch.object(bft.BuildkiteTestEngineClient, 'get_recent_runs')
    @patch.object(bft.BuildkiteTestEngineClient, 'get_failed_executions')
    def test_enrich_flaky_tests_multiple_failures(self, mock_get_executions, mock_get_runs):
        """Test enrichment with multiple different failures."""
        mock_get_runs.return_value = [
            {"id": "run-1", "url": "https://example.com/run-1", "created_at": "2026-03-31T10:00:00Z"},
            {"id": "run-2", "url": "https://example.com/run-2", "created_at": "2026-03-31T09:00:00Z"}
        ]

        # Different failures in each run
        mock_get_executions.side_effect = [
            [{"test_id": "test-123", "failure_reason": "Error A"}],
            [{"test_id": "test-123", "failure_reason": "Error B"}]
        ]

        flaky_tests = [{"id": "test-123", "name": "test_foo"}]

        result = self.client.enrich_flaky_tests_with_failures("suite-id", flaky_tests)

        # Should have both failures
        assert len(result[0]["failure_examples"]) == 2
        # Each message is now a list of strings
        messages = [f["message"] for f in result[0]["failure_examples"]]
        assert any("Error A" in msg for msg in messages[0])
        assert any("Error B" in msg for msg in messages[1])

    @patch.object(bft.BuildkiteTestEngineClient, 'get_recent_runs')
    @patch.object(bft.BuildkiteTestEngineClient, 'get_failed_executions')
    def test_enrich_flaky_tests_no_matching_test_id(self, mock_get_executions, mock_get_runs):
        """Test enrichment when failed execution doesn't match any flaky test."""
        mock_get_runs.return_value = [
            {"id": "run-1", "url": "https://example.com/run-1", "created_at": "2026-03-31T10:00:00Z"}
        ]

        mock_get_executions.return_value = [
            {"test_id": "other-test", "failure_reason": "Error"}
        ]

        flaky_tests = [{"id": "test-123", "name": "test_foo"}]

        result = self.client.enrich_flaky_tests_with_failures("suite-id", flaky_tests)

        # Should have no failure examples
        assert len(result[0]["failure_examples"]) == 0

    @patch.object(bft.BuildkiteTestEngineClient, 'get_recent_runs')
    @patch.object(bft.BuildkiteTestEngineClient, 'get_failed_executions')
    def test_enrich_flaky_tests_max_runs_limit(self, mock_get_executions, mock_get_runs):
        """Test that max_runs parameter is respected."""
        mock_get_runs.return_value = []

        flaky_tests = [{"id": "test-123", "name": "test_foo"}]

        self.client.enrich_flaky_tests_with_failures("suite-id", flaky_tests, max_runs=25)

        # Check that get_recent_runs was called with correct limit
        mock_get_runs.assert_called_once_with("suite-id", limit=25)

    @patch.object(bft.BuildkiteTestEngineClient, 'get_recent_runs')
    @patch.object(bft.BuildkiteTestEngineClient, 'get_failed_executions')
    def test_enrich_with_failure_expanded(self, mock_get_executions, mock_get_runs):
        """Test enrichment uses failure_expanded when available."""
        mock_get_runs.return_value = [
            {"id": "run-1", "url": "https://example.com/run-1", "created_at": "2026-04-01T10:00:00Z"}
        ]

        # Mock execution with failure_expanded (real API format: array of objects with backtrace)
        mock_get_executions.return_value = [
            {
                "test_id": "test-123",
                "failure_reason": "Got 1 failure",  # Truncated version
                "failure_expanded": [
                    {
                        "backtrace": [
                            "AssertionError: Expected 5 but got 4",
                            "  File 'test.py', line 42, in test_foo",
                            "    assert result == 5"
                        ],
                        "expanded": ["AssertionError: Expected 5 but got 4"]
                    }
                ]
            }
        ]

        flaky_tests = [{"id": "test-123", "name": "test_foo"}]
        result = self.client.enrich_flaky_tests_with_failures("suite-id", flaky_tests)

        # Should use failure_expanded (full trace), not failure_reason (truncated)
        assert len(result[0]["failure_examples"]) == 1
        failure = result[0]["failure_examples"][0]
        # Message should be a list of strings
        assert isinstance(failure["message"], list)
        assert len(failure["message"]) == 3
        assert failure["message"][0] == "AssertionError: Expected 5 but got 4"
        assert "File 'test.py', line 42" in failure["message"][1]

    @patch.object(bft.BuildkiteTestEngineClient, 'get_recent_runs')
    @patch.object(bft.BuildkiteTestEngineClient, 'get_failed_executions')
    def test_enrich_fallback_to_failure_reason(self, mock_get_executions, mock_get_runs):
        """Test enrichment falls back to failure_reason when failure_expanded is null."""
        mock_get_runs.return_value = [
            {"id": "run-1", "url": "https://example.com/run-1", "created_at": "2026-04-01T10:00:00Z"}
        ]

        # Mock execution with null failure_expanded (older executions)
        mock_get_executions.return_value = [
            {
                "test_id": "test-123",
                "failure_reason": "Got 1 failure and 0 errors.",
                "failure_expanded": None
            }
        ]

        flaky_tests = [{"id": "test-123", "name": "test_foo"}]
        result = self.client.enrich_flaky_tests_with_failures("suite-id", flaky_tests)

        # Should use failure_reason as fallback
        assert len(result[0]["failure_examples"]) == 1
        failure = result[0]["failure_examples"][0]
        # Should be list even for simple string (split by newlines)
        assert isinstance(failure["message"], list)
        assert "Got 1 failure and 0 errors." in failure["message"]

    @patch.object(bft.BuildkiteTestEngineClient, 'get_recent_runs')
    @patch.object(bft.BuildkiteTestEngineClient, 'get_failed_executions')
    def test_enrich_empty_failure_expanded_array(self, mock_get_executions, mock_get_runs):
        """Test enrichment handles empty failure_expanded array."""
        mock_get_runs.return_value = [
            {"id": "run-1", "url": "https://example.com/run-1", "created_at": "2026-04-01T10:00:00Z"}
        ]

        # Mock execution with empty failure_expanded array
        mock_get_executions.return_value = [
            {
                "test_id": "test-123",
                "failure_reason": "Test failed",
                "failure_expanded": []
            }
        ]

        flaky_tests = [{"id": "test-123", "name": "test_foo"}]
        result = self.client.enrich_flaky_tests_with_failures("suite-id", flaky_tests)

        # Should fall back to failure_reason
        assert len(result[0]["failure_examples"]) == 1
        failure = result[0]["failure_examples"][0]
        # Should be a list even for simple string
        assert isinstance(failure["message"], list)
        assert "Test failed" in failure["message"]

    @patch.object(bft.BuildkiteTestEngineClient, 'get_recent_runs')
    @patch.object(bft.BuildkiteTestEngineClient, 'get_failed_executions')
    def test_enrich_no_failure_info(self, mock_get_executions, mock_get_runs):
        """Test enrichment when no failure info is available."""
        mock_get_runs.return_value = [
            {"id": "run-1", "url": "https://example.com/run-1", "created_at": "2026-04-01T10:00:00Z"}
        ]

        # Mock execution with no failure info
        mock_get_executions.return_value = [
            {
                "test_id": "test-123",
                "failure_reason": None,
                "failure_expanded": None
            }
        ]

        flaky_tests = [{"id": "test-123", "name": "test_foo"}]
        result = self.client.enrich_flaky_tests_with_failures("suite-id", flaky_tests)

        # Should have no failure examples
        assert len(result[0]["failure_examples"]) == 0

    @patch.object(bft.BuildkiteTestEngineClient, 'get_recent_runs')
    @patch.object(bft.BuildkiteTestEngineClient, 'get_failed_executions')
    def test_enrich_respects_max_examples_per_test(self, mock_get_executions, mock_get_runs):
        """Test that enrichment caps failure examples per test."""
        # Mock runs
        mock_get_runs.return_value = [
            {"id": f"run-{i}", "url": f"http://example.com/run/{i}", "created_at": "2024-01-01"}
            for i in range(10)
        ]

        # Mock executions - many failures for the same test
        mock_get_executions.return_value = [
            {
                "test_id": "test-123",
                "failure_reason": f"Failure {i}"
            }
            for i in range(10)
        ]

        flaky_tests = [{"id": "test-123", "name": "test_foo"}]
        result = self.client.enrich_flaky_tests_with_failures(
            "suite-id", flaky_tests, max_runs=10, max_examples_per_test=3
        )

        # Should cap at 3 examples even though more were available
        assert len(result[0]["failure_examples"]) == 3

    @patch.object(bft.BuildkiteTestEngineClient, 'get_recent_runs')
    @patch.object(bft.BuildkiteTestEngineClient, 'get_failed_executions')
    def test_enrich_stops_early_when_all_tests_have_max_examples(self, mock_get_executions, mock_get_runs):
        """Test that enrichment short-circuits when all tests reach max examples."""
        # Mock 100 runs
        mock_get_runs.return_value = [
            {"id": f"run-{i}", "url": f"http://example.com/run/{i}", "created_at": "2024-01-01"}
            for i in range(100)
        ]

        # Mock executions - each run has one failure
        call_count = 0
        def mock_executions_side_effect(suite_id, run_id):
            nonlocal call_count
            call_count += 1
            return [{
                "test_id": "test-123",
                "failure_reason": f"Failure {call_count}"
            }]

        mock_get_executions.side_effect = mock_executions_side_effect

        flaky_tests = [{"id": "test-123", "name": "test_foo"}]
        result = self.client.enrich_flaky_tests_with_failures(
            "suite-id", flaky_tests, max_runs=100, max_examples_per_test=3
        )

        # Should have capped at 3 examples
        assert len(result[0]["failure_examples"]) == 3

        # Should have stopped early (only 3 API calls, not 100)
        assert call_count == 3

    @patch.object(bft.BuildkiteTestEngineClient, 'get_recent_runs')
    @patch.object(bft.BuildkiteTestEngineClient, 'get_failed_executions')
    def test_enrich_continues_until_all_tests_have_examples(self, mock_get_executions, mock_get_runs):
        """Test that enrichment continues for tests that still need examples."""
        # Mock runs
        mock_get_runs.return_value = [
            {"id": f"run-{i}", "url": f"http://example.com/run/{i}", "created_at": "2024-01-01"}
            for i in range(10)
        ]

        # Mock executions - alternate between two tests
        call_count = 0
        def mock_executions_side_effect(suite_id, run_id):
            nonlocal call_count
            call_count += 1
            # First 3 calls return test-123, rest return test-456
            test_id = "test-123" if call_count <= 3 else "test-456"
            return [{
                "test_id": test_id,
                "failure_reason": f"Failure {call_count}"
            }]

        mock_get_executions.side_effect = mock_executions_side_effect

        flaky_tests = [
            {"id": "test-123", "name": "test_foo"},
            {"id": "test-456", "name": "test_bar"}
        ]
        result = self.client.enrich_flaky_tests_with_failures(
            "suite-id", flaky_tests, max_runs=10, max_examples_per_test=3
        )

        # Both tests should have 3 examples
        assert len(result[0]["failure_examples"]) == 3
        assert len(result[1]["failure_examples"]) == 3

        # Should have made 6 calls total (3 for each test)
        assert call_count == 6


class TestNullFieldHandling:
    """Tests for handling null file_name and location fields."""

    def setup_method(self):
        """Set up test fixtures."""
        self.manager = bft.GitHubIssueManager("test-org/test-repo")

    @patch.object(bft.GitHubIssueManager, '_run_gh_command')
    def test_create_issue_with_null_file_name(self, mock_gh):
        """Test creating issue when file_name is null."""
        mock_gh.return_value = "https://github.com/test-org/test-repo/issues/999"

        test_data = {
            "name": "TestFetch",
            "scope": "github.com/elastic/beats/module",
            "location": None,
            "file_name": None,  # Null file_name from older collector
            "web_url": "https://buildkite.com/test",
            "instances": 6,
            "failure_examples": []
        }

        result = self.manager.create_issue(test_data)

        assert result == "https://github.com/test-org/test-repo/issues/999"
        args = mock_gh.call_args[0][0]
        body_index = args.index("--body") + 1
        body = args[body_index]

        # Should show N/A for null fields
        assert "**File:** N/A" in body or "**File:** None" in body
        assert "**Location:** N/A" in body or "**Location:** None" in body

    def test_extract_test_info_with_nulls(self):
        """Test _extract_test_info handles null values correctly."""
        test_data = {
            "name": "test_foo",
            "scope": "module.Test",
            "location": None,
            "file_name": None,
            "web_url": "https://example.com"
        }

        name, scope, location, file_name, web_url = bft.GitHubIssueManager._extract_test_info(test_data)

        assert name == "test_foo"
        assert scope == "module.Test"
        assert location == "N/A"  # Should default to N/A
        assert file_name == "N/A"  # Should default to N/A
        assert web_url == "https://example.com"

    def test_extract_test_info_with_values(self):
        """Test _extract_test_info with valid values."""
        test_data = {
            "name": "test_foo",
            "scope": "module.Test",
            "location": "test.py:42",
            "file_name": "test.py",
            "web_url": "https://example.com"
        }

        name, scope, location, file_name, web_url = bft.GitHubIssueManager._extract_test_info(test_data)

        assert name == "test_foo"
        assert scope == "module.Test"
        assert location == "test.py:42"
        assert file_name == "test.py"
        assert web_url == "https://example.com"


class TestGitHubIssueWithFailures:
    """Tests for GitHub issue creation with failure examples."""

    def setup_method(self):
        """Set up test fixtures."""
        self.manager = bft.GitHubIssueManager("test-org/test-repo")

    @patch.object(bft.GitHubIssueManager, '_run_gh_command')
    def test_create_issue_with_dict_failure_examples(self, mock_gh):
        """Test creating issue with dict-based failure examples."""
        mock_gh.return_value = "https://github.com/test-org/test-repo/issues/999"

        test_data = {
            "name": "test_foo",
            "scope": "module.Test",
            "location": "test.py:42",
            "file_name": "test.py",
            "web_url": "https://buildkite.com/test",
            "instances": 5,
            "latest_occurrence_at": "2026-03-31T10:00:00Z",
            "failure_examples": [
                {
                    "message": ["AssertionError: Expected 5 but got 4", "  File 'test.py', line 42"],
                    "run_url": "https://example.com/run-1",
                    "run_time": "2026-03-31T10:00:00Z"
                }
            ]
        }

        result = self.manager.create_issue(test_data)

        assert result == "https://github.com/test-org/test-repo/issues/999"
        mock_gh.assert_called_once()

        # Check that the body contains the failure examples
        args = mock_gh.call_args[0][0]
        body_index = args.index("--body") + 1
        body = args[body_index]

        assert "Failure Examples" in body
        assert "https://example.com/run-1" in body
        assert "AssertionError: Expected 5 but got 4" in body
        # Check that run URL is NOT inside code block (should be before it)
        assert "**Run:**" in body
        assert "**Stacktrace:**" in body

    @patch.object(bft.GitHubIssueManager, '_run_gh_command')
    def test_create_issue_with_multiple_failure_examples(self, mock_gh):
        """Test creating issue with multiple failure examples."""
        mock_gh.return_value = "https://github.com/test-org/test-repo/issues/999"

        test_data = {
            "name": "test_foo",
            "scope": "module.Test",
            "location": "test.py:42",
            "file_name": "test.py",
            "web_url": "https://buildkite.com/test",
            "failure_examples": [
                {
                    "message": ["Error A"],
                    "run_url": "https://example.com/run-1",
                    "run_time": "2026-03-31T10:00:00Z"
                },
                {
                    "message": ["Error B"],
                    "run_url": "https://example.com/run-2",
                    "run_time": "2026-03-31T09:00:00Z"
                },
                {
                    "message": ["Error C"],
                    "run_url": "https://example.com/run-3",
                    "run_time": "2026-03-31T08:00:00Z"
                }
            ]
        }

        self.manager.create_issue(test_data)

        args = mock_gh.call_args[0][0]
        body_index = args.index("--body") + 1
        body = args[body_index]

        # Should only show first 3 examples
        assert "**Example 1:**" in body
        assert "**Example 2:**" in body
        assert "**Example 3:**" in body
        assert "Error A" in body
        assert "Error B" in body
        assert "Error C" in body

    @patch.object(bft.GitHubIssueManager, '_run_gh_command')
    def test_create_issue_no_failure_examples(self, mock_gh):
        """Test creating issue with no failure examples."""
        mock_gh.return_value = "https://github.com/test-org/test-repo/issues/999"

        test_data = {
            "name": "test_foo",
            "scope": "module.Test",
            "location": "test.py:42",
            "file_name": "test.py",
            "web_url": "https://buildkite.com/test",
            "failure_examples": []
        }

        result = self.manager.create_issue(test_data)
        assert result == "https://github.com/test-org/test-repo/issues/999"

        args = mock_gh.call_args[0][0]
        body_index = args.index("--body") + 1
        body = args[body_index]

        # Should not have Failure Examples section
        assert "Failure Examples" not in body

    @patch.object(bft.GitHubIssueManager, '_run_gh_command')
    def test_create_issue_backward_compatible_string_failures(self, mock_gh):
        """Test backward compatibility with string-based failure examples."""
        mock_gh.return_value = "https://github.com/test-org/test-repo/issues/999"

        test_data = {
            "name": "test_foo",
            "scope": "module.Test",
            "location": "test.py:42",
            "file_name": "test.py",
            "web_url": "https://buildkite.com/test",
            "failure_examples": ["String-based error message"]
        }

        result = self.manager.create_issue(test_data)

        assert result == "https://github.com/test-org/test-repo/issues/999"
        args = mock_gh.call_args[0][0]
        body_index = args.index("--body") + 1
        body = args[body_index]

        assert "String-based error message" in body


class TestCLIArgumentsNew:
    """Tests for new CLI arguments."""

    @patch.object(bft.BuildkiteTestEngineClient, 'get_flaky_tests')
    @patch.object(bft.BuildkiteTestEngineClient, 'enrich_flaky_tests_with_failures')
    def test_max_runs_argument(self, mock_enrich, mock_get_tests):
        """Test --max-runs argument is passed correctly."""
        # Return at least one test so enrichment is called
        mock_get_tests.return_value = [{"id": "test-1", "name": "test_foo"}]
        mock_enrich.return_value = [{"id": "test-1", "name": "test_foo", "failure_examples": []}]

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('sys.argv', [
                'buildkite_flaky_report.py', 'test-suite-id',
                '--org', 'test-org', '--api-token', 'test-token',
                '--max-runs', '100', '--output-dir', tmpdir
            ]):
                bft.main()

        # Check that enrich was called with max_runs=100
        mock_enrich.assert_called_once()
        call_kwargs = mock_enrich.call_args[1]
        assert call_kwargs.get('max_runs') == 100

    @patch.object(bft.BuildkiteTestEngineClient, 'get_flaky_tests')
    def test_debug_argument_enables_logging(self, mock_get_tests):
        """Test --debug argument enables debug logging."""
        mock_get_tests.return_value = []

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('sys.argv', [
                'buildkite_flaky_report.py', 'test-suite-id',
                '--org', 'test-org', '--api-token', 'test-token',
                '--debug', '--output-dir', tmpdir
            ]):
                with patch('logging.basicConfig') as mock_logging:
                    bft.main()

                    # Check that debug level was set
                    mock_logging.assert_called_once()
                    call_kwargs = mock_logging.call_args[1]
                    assert call_kwargs['level'] == logging.DEBUG

    def test_max_runs_validation_negative(self, caplog):
        """Test that negative max-runs value is rejected."""
        with caplog.at_level(logging.ERROR):
            with patch('sys.argv', [
                'buildkite_flaky_report.py', 'test-suite-id',
                '--org', 'test-org', '--api-token', 'test-token',
                '--max-runs', '-1'
            ]):
                with pytest.raises(SystemExit) as exc_info:
                    bft.main()

        assert exc_info.value.code == 1
        assert '--max-runs must be >= 0' in caplog.text

    @patch.object(bft.BuildkiteTestEngineClient, 'get_flaky_tests')
    @patch.object(bft.BuildkiteTestEngineClient, 'enrich_flaky_tests_with_failures')
    def test_default_max_runs_value(self, mock_enrich, mock_get_tests):
        """Test that default max-runs value is 50."""
        # Return at least one test so enrichment is called
        mock_get_tests.return_value = [{"id": "test-1", "name": "test_foo"}]
        mock_enrich.return_value = [{"id": "test-1", "name": "test_foo", "failure_examples": []}]

        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('sys.argv', [
                'buildkite_flaky_report.py', 'test-suite-id',
                '--org', 'test-org', '--api-token', 'test-token',
                '--output-dir', tmpdir
            ]):
                bft.main()

        # Check that enrich was called with default max_runs=50
        mock_enrich.assert_called_once()
        call_kwargs = mock_enrich.call_args[1]
        assert call_kwargs.get('max_runs') == 50


class TestHelperMethods:
    """Tests for refactored helper methods."""

    def test_extract_failure_message_from_expanded(self):
        """Test extracting failure message from failure_expanded."""
        execution = {
            "test_id": "test-123",
            "failure_reason": "Got 1 failure",
            "failure_expanded": [
                {
                    "backtrace": [
                        "Line 1",
                        "Line 2",
                        "Line 3"
                    ],
                    "expanded": ["Summary"]
                }
            ]
        }

        result = bft.BuildkiteTestEngineClient._extract_failure_message(execution)

        assert result is not None
        assert isinstance(result, list)
        assert len(result) == 3
        assert result[0] == "Line 1"
        assert result[1] == "Line 2"

    def test_extract_failure_message_from_reason(self):
        """Test extracting failure message from failure_reason as fallback."""
        execution = {
            "test_id": "test-123",
            "failure_reason": "Error line 1\nError line 2",
            "failure_expanded": None
        }

        result = bft.BuildkiteTestEngineClient._extract_failure_message(execution)

        assert result is not None
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0] == "Error line 1"
        assert result[1] == "Error line 2"

    def test_extract_failure_message_empty_expanded(self):
        """Test fallback when failure_expanded is empty."""
        execution = {
            "test_id": "test-123",
            "failure_reason": "Fallback error",
            "failure_expanded": []
        }

        result = bft.BuildkiteTestEngineClient._extract_failure_message(execution)

        assert result is not None
        assert "Fallback error" in result

    def test_extract_failure_message_no_info(self):
        """Test returns None when no failure info available."""
        execution = {
            "test_id": "test-123",
            "failure_reason": None,
            "failure_expanded": None
        }

        result = bft.BuildkiteTestEngineClient._extract_failure_message(execution)

        assert result is None

    def test_is_duplicate_failure_exact_match(self):
        """Test duplicate detection with exact match."""
        failure_lines = ["Line 1", "Line 2", "Line 3"]
        existing_failures = [
            {"message": ["Line 1", "Line 2", "Line 3"], "run_url": "http://example.com"}
        ]

        result = bft.BuildkiteTestEngineClient._is_duplicate_failure(failure_lines, existing_failures)

        assert result is True

    def test_is_duplicate_failure_partial_match(self):
        """Test duplicate detection uses only first N lines."""
        failure_lines = ["Same 1", "Same 2", "Different 3"]
        existing_failures = [
            {"message": ["Same 1", "Same 2", "Different X"], "run_url": "http://example.com"}
        ]

        # Should match based on first 10 lines (even though line 3 differs)
        result = bft.BuildkiteTestEngineClient._is_duplicate_failure(failure_lines, existing_failures, signature_lines=2)

        assert result is True

    def test_is_duplicate_failure_no_match(self):
        """Test duplicate detection returns False for different failures."""
        failure_lines = ["Different 1", "Different 2"]
        existing_failures = [
            {"message": ["Line 1", "Line 2"], "run_url": "http://example.com"}
        ]

        result = bft.BuildkiteTestEngineClient._is_duplicate_failure(failure_lines, existing_failures)

        assert result is False

    def test_is_duplicate_failure_empty_existing(self):
        """Test duplicate detection with no existing failures."""
        failure_lines = ["Line 1", "Line 2"]
        existing_failures = []

        result = bft.BuildkiteTestEngineClient._is_duplicate_failure(failure_lines, existing_failures)

        assert result is False

    def test_format_failure_examples_with_list_messages(self):
        """Test formatting failure examples with list messages."""
        failures = [
            {
                "message": ["Line 1", "Line 2", "Line 3"],
                "run_url": "http://example.com/run/1",
                "run_time": "2024-01-01T10:00:00Z"
            }
        ]

        result = bft.GitHubIssueManager._format_failure_examples_markdown(failures)

        assert "### Failure Examples" in result
        assert "Example 1:" in result
        assert "http://example.com/run/1" in result
        assert "2024-01-01T10:00:00Z" in result
        assert "Line 1" in result
        assert "Line 2" in result
        assert "Line 3" in result
        assert "```" in result

    def test_format_failure_examples_with_string_messages(self):
        """Test formatting failure examples with string messages (backward compatibility)."""
        failures = [
            {
                "message": "Single line error",
                "run_url": "http://example.com/run/1"
            }
        ]

        result = bft.GitHubIssueManager._format_failure_examples_markdown(failures)

        assert "### Failure Examples" in result
        assert "Single line error" in result

    def test_format_failure_examples_respects_max_limit(self):
        """Test that only max_examples are included."""
        failures = [
            {"message": ["Error 1"], "run_url": "http://example.com/1"},
            {"message": ["Error 2"], "run_url": "http://example.com/2"},
            {"message": ["Error 3"], "run_url": "http://example.com/3"},
            {"message": ["Error 4"], "run_url": "http://example.com/4"},
            {"message": ["Error 5"], "run_url": "http://example.com/5"},
        ]

        result = bft.GitHubIssueManager._format_failure_examples_markdown(failures, max_examples=3)

        # Should only include first 3
        assert "Example 1:" in result
        assert "Example 2:" in result
        assert "Example 3:" in result
        assert "Example 4:" not in result
        assert "Example 5:" not in result

    def test_format_failure_examples_empty_list(self):
        """Test formatting returns empty string for empty list."""
        result = bft.GitHubIssueManager._format_failure_examples_markdown([])

        assert result == ""

    def test_format_failure_examples_without_metadata(self):
        """Test formatting works without run_url and run_time."""
        failures = [
            {"message": ["Error occurred"]}
        ]

        result = bft.GitHubIssueManager._format_failure_examples_markdown(failures)

        assert "### Failure Examples" in result
        assert "Error occurred" in result
        # Should not have Run: or Time: sections
        assert "**Run:**" not in result
        assert "**Time:**" not in result


class TestNewFixes:
    """Tests for recent bug fixes and improvements."""

    def setup_method(self):
        """Set up test fixtures."""
        self.client = bft.BuildkiteTestEngineClient("test-token", "test-org")
        self.manager = bft.GitHubIssueManager("test-org/test-repo")

    @patch.object(bft.BuildkiteTestEngineClient, '_make_request')
    def test_get_recent_runs_pagination(self, mock_request):
        """Test that get_recent_runs paginates correctly for large limits."""
        # Mock pagination: 3 pages of 100, then partial page
        mock_request.side_effect = [
            [{"id": f"run-{i}"} for i in range(100)],  # Page 1: 100 items
            [{"id": f"run-{i}"} for i in range(100, 200)],  # Page 2: 100 items
            [{"id": f"run-{i}"} for i in range(200, 250)],  # Page 3: 50 items (partial)
        ]

        result = self.client.get_recent_runs("suite-id", limit=250)

        assert len(result) == 250
        assert mock_request.call_count == 3
        # Verify pagination was used - check the params dict (second arg)
        # call_args_list[i][0] is positional args tuple, [0][1] is second positional arg (params)
        assert mock_request.call_args_list[0][0][1]["page"] == 1
        assert mock_request.call_args_list[1][0][1]["page"] == 2
        assert mock_request.call_args_list[2][0][1]["page"] == 3

    @patch.object(bft.BuildkiteTestEngineClient, '_make_request')
    def test_get_recent_runs_respects_limit(self, mock_request):
        """Test that get_recent_runs returns only up to limit."""
        # Return more than requested
        mock_request.return_value = [{"id": f"run-{i}"} for i in range(100)]

        result = self.client.get_recent_runs("suite-id", limit=50)

        # Should return only 50 even though 100 were available
        assert len(result) == 50

    @patch.object(bft.BuildkiteTestEngineClient, 'get_recent_runs')
    @patch.object(bft.BuildkiteTestEngineClient, 'get_failed_executions')
    def test_enrich_with_max_runs_zero_skips_enrichment(self, mock_get_executions, mock_get_runs):
        """Test that max_runs=0 skips enrichment entirely."""
        flaky_tests = [{"id": "test-123", "name": "test_foo"}]

        result = self.client.enrich_flaky_tests_with_failures("suite-id", flaky_tests, max_runs=0)

        # Should not call any API methods
        mock_get_runs.assert_not_called()
        mock_get_executions.assert_not_called()

        # Should still initialize failure_examples as empty
        assert result[0]["failure_examples"] == []

    def test_build_markdown_sanitizes_failure_examples(self):
        """Test that _build_markdown removes failure_examples from JSON details."""
        test_data = {
            "id": "test-123",
            "name": "test_foo",
            "failure_examples": [
                {"message": "A" * 10000, "run_url": "http://example.com"},  # Huge message
                {"message": "B" * 10000, "run_url": "http://example.com"},
            ]
        }

        fields = {"Test Name": "test_foo"}
        markdown = self.manager._build_markdown("Test", fields, test_data)

        # Should not contain the huge failure_examples in JSON
        assert "failure_examples" not in markdown or "failure_examples_count" in markdown
        # Should have count instead
        assert "failure_examples_count" in markdown or "failure_examples" not in markdown

    def test_max_runs_validation_zero_is_valid(self):
        """Test that max_runs=0 is accepted (disables enrichment)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('sys.argv', [
                'buildkite_flaky_report.py', 'test-suite-id',
                '--org', 'test-org', '--api-token', 'test-token',
                '--max-runs', '0', '--output-dir', tmpdir
            ]):
                with patch.object(bft.BuildkiteTestEngineClient, 'get_flaky_tests', return_value=[]):
                    # Should not raise - max_runs=0 is valid
                    bft.main()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
