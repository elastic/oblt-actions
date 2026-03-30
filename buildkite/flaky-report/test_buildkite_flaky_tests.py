#!/usr/bin/env python3
"""
Unit tests for buildkite_flaky_tests.py

Run with: pytest test_buildkite_flaky_tests.py -v
"""

import json
import pytest
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, call
import tempfile
import os

# Import the module to test
import buildkite_flaky_tests as bft


class TestBuildkiteTestEngineClient:
    """Tests for BuildkiteTestEngineClient class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.client = bft.BuildkiteTestEngineClient("test-token", "test-org")

    def test_initialization(self):
        """Test client initialization."""
        assert self.client.api_token == "test-token"
        assert self.client.org_slug == "test-org"
        assert self.client.base_url == "https://api.buildkite.com/v2"
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

    @patch.object(bft.BuildkiteTestEngineClient, '_make_request')
    def test_get_test_suite(self, mock_request):
        """Test get_test_suite method."""
        result = self.client.get_test_suite("test-suite")

        assert result == {"slug": "test-suite"}

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
    @patch('builtins.print')
    def test_get_flaky_tests_with_date_filter(self, mock_print, mock_request):
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
    @patch('builtins.print')
    def test_get_flaky_tests_date_filter_with_current_endpoint(self, mock_print, mock_request):
        """Test that date filtering warns with current endpoint."""
        mock_request.return_value = [
            {"id": "1", "name": "test1", "labels": ["flaky"]}
        ]

        result = self.client.get_flaky_tests(
            "suite-id",
            days=7,
            use_deprecated_endpoint=False
        )

        # Should return all tests with a warning
        assert len(result) == 1
        mock_print.assert_called_once()
        assert "Cannot filter by days" in mock_print.call_args[0][0]

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


class TestGitHubIssueManager:
    """Tests for GitHubIssueManager class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.manager = bft.GitHubIssueManager("test-org/test-repo")

    def test_initialization(self):
        """Test GitHub manager initialization."""
        assert self.manager.repo == "test-org/test-repo"

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

        with pytest.raises(Exception) as exc_info:
            self.manager._run_gh_command(["issue", "list"])

        assert "gh command failed" in str(exc_info.value)

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


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
