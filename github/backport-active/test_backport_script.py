import os
import json
import unittest
from unittest.mock import patch, MagicMock

import backport_script

class TestBackportScript(unittest.TestCase):
    def setUp(self):
        # Set up common environment variables
        os.environ['GITHUB_TOKEN'] = 'my-token'
        os.environ['PR_NUMBER'] = '123'
        os.environ['REPOSITORY'] = 'owner/repo'
        # Default: assume config URL returns valid JSON
        os.environ['BACKPORTS_URL'] = 'https://branches.json'

    @patch('backport_script.requests.get')
    @patch('backport_script.requests.post')
    def test_backport_active_all(self, mock_post, mock_get):
        # In this scenario, the PR label "backport-active-all" triggers backporting on all branches (except 'main' and '7.17').
        os.environ['PR_LABELS'] = json.dumps([{"name": "backport-active-all"}])
        config_response = MagicMock()
        config_data = {'branches': ['main', '7.17', '8.16', '8.17', '9.0']}
        config_response.status_code = 200
        config_response.json.return_value = config_data

        # Patch requests.get: if the URL matches BACKPORTS_URL, return our dummy config_response.
        def get_side_effect(url, headers=None, timeout=None):
            if url == os.environ['BACKPORTS_URL']:
                return config_response
            else:
                dummy = MagicMock()
                dummy.status_code = 404
                return dummy
        mock_get.side_effect = get_side_effect

        # Simulate successful posting of the comment.
        post_response = MagicMock()
        post_response.status_code = 201
        mock_post.return_value = post_response

        exit_code = backport_script.main()
        self.assertEqual(exit_code, 0)

        # We expect branches other than 'main' or '7.17' to be targeted:
        expected_branches = ['8.16', '8.17', '9.0']
        expected_comment = f"@mergifyio backport {' '.join(expected_branches)}"

        # Verify that a comment containing the expected branches has been posted.
        mock_post.assert_called_once()
        _, kwargs = mock_post.call_args
        body = kwargs.get('json', {}).get('body', '')
        self.assertIn(expected_comment, body)

    @patch('backport_script.requests.get')
    @patch('backport_script.requests.post')
    def test_backport_active_8(self, mock_post, mock_get):
        # Change PR_LABELS so that only "backport-active-8" is present.
        os.environ['PR_LABELS'] = json.dumps([{"name": "backport-active-8"}])
        config_response = MagicMock()
        config_data = {'branches': ['8.0', '8.1', 'main', '7.17']}
        config_response.status_code = 200
        config_response.json.return_value = config_data

        def get_side_effect(url, headers=None, timeout=None):
            if url == os.environ['BACKPORTS_URL']:
                return config_response
            else:
                dummy = MagicMock()
                dummy.status_code = 404
                return dummy
        mock_get.side_effect = get_side_effect

        post_response = MagicMock()
        post_response.status_code = 201
        mock_post.return_value = post_response

        exit_code = backport_script.main()
        self.assertEqual(exit_code, 0)

        # Expect only branches starting with "8." to be selected.
        expected_branches = ['8.0', '8.1']
        expected_comment = f"@mergifyio backport {' '.join(expected_branches)}"

        mock_post.assert_called_once()
        _, kwargs = mock_post.call_args
        body = kwargs.get('json', {}).get('body', '')
        self.assertIn(expected_comment, body)

    @patch('backport_script.requests.get')
    @patch('backport_script.requests.post')
    def test_backport_active_9(self, mock_post, mock_get):
        # Change PR_LABELS so that only "backport-active-9" is present.
        os.environ['PR_LABELS'] = json.dumps([{"name": "backport-active-9"}])
        config_response = MagicMock()
        config_data = {'branches': ['9.0', '8.1', 'main', '7.17']}
        config_response.status_code = 200
        config_response.json.return_value = config_data

        def get_side_effect(url, headers=None, timeout=None):
            if url == os.environ['BACKPORTS_URL']:
                return config_response
            else:
                dummy = MagicMock()
                dummy.status_code = 404
                return dummy
        mock_get.side_effect = get_side_effect

        post_response = MagicMock()
        post_response.status_code = 201
        mock_post.return_value = post_response

        exit_code = backport_script.main()
        self.assertEqual(exit_code, 0)

        # Expect only branches starting with "9." to be selected.
        expected_branches = ['9.0']
        expected_comment = f"@mergifyio backport {' '.join(expected_branches)}"

        mock_post.assert_called_once()
        _, kwargs = mock_post.call_args
        body = kwargs.get('json', {}).get('body', '')
        self.assertIn(expected_comment, body)

    @patch('backport_script.requests.get')
    @patch('backport_script.requests.post')
    def test_no_backport_labels(self, mock_post, mock_get):
        # If there are no backport-related labels, no backport comment should be posted.
        os.environ['PR_LABELS'] = json.dumps([{"name": "enhancement"}, {"name": "bug"}])
        config_response = MagicMock()
        config_data = {'branches': ['main', '7.17', '8.16']}
        config_response.status_code = 200
        config_response.json.return_value = config_data

        def get_side_effect(url, headers=None, timeout=None):
            if url == os.environ['BACKPORTS_URL']:
                return config_response
            else:
                dummy = MagicMock()
                dummy.status_code = 404
                return dummy
        mock_get.side_effect = get_side_effect

        # In this case, no POST should be made because no backport label is present.
        exit_code = backport_script.main()
        self.assertEqual(exit_code, 0)
        mock_post.assert_not_called()


if __name__ == '__main__':
    unittest.main()
