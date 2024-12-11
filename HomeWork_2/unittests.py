import unittest
from unittest.mock import patch, mock_open, MagicMock
from hw2 import read_config, get_commit_tree, get_commit_changes, generate_mermaid_code, write_output, main


class TestHW2(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='<config><repo_path>/path/to/repo</repo_path><output_path>/path/to/output</output_path></config>')
    def test_read_config(self, mock_file):
        config = read_config('dummy_path')
        expected_config = {
            'repo_path': '/path/to/repo',
            'output_path': '/path/to/output'
        }
        self.assertEqual(config, expected_config)

    @patch('subprocess.run')
    def test_get_commit_tree(self, mock_run):
        # Mocking subprocess.run calls for `git log` and `git show`
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout='abc123 Commit message 1\nabc456 Commit message 2\n'),
            MagicMock(returncode=0, stdout='A\tfile1.txt\nM\tfile2.txt\n'),
            MagicMock(returncode=0, stdout='D\tfile3.txt\n'),
        ]

        commit_info = get_commit_tree('/path/to/repo')
        expected_commit_info = {
            'abc123': {
                'message': 'Commit message 1',
                'children': [],
                'changes': ['A\tfile1.txt', 'M\tfile2.txt']
            },
            'abc456': {
                'message': 'Commit message 2',
                'children': [],
                'changes': ['D\tfile3.txt']
            }
        }
        self.assertEqual(commit_info, expected_commit_info)

    @patch('subprocess.run')
    def test_get_commit_changes(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout='A\tfile1.txt\nM\tfile2.txt\n')
        changes = get_commit_changes('/path/to/repo', 'abc123')
        expected_changes = ['A\tfile1.txt', 'M\tfile2.txt']
        self.assertEqual(changes, expected_changes)

    def test_generate_mermaid_code(self):
        commit_info = {
            'abc123': {
                'message': 'Commit message 1',
                'children': [],
                'changes': ['A\tfile1.txt', 'M\tfile2.txt']
            },
            'abc456': {
                'message': 'Commit message 2',
                'children': [],
                'changes': ['D\tfile3.txt']
            }
        }

        expected_output = """graph TD
    abc123["Commit message 1\\nabc123"]
    abc123 --> "file1.txt (A)"
    abc123 --> "file2.txt (M)"
    abc456["Commit message 2\\nabc456"]
    abc123 --> abc456
    abc456 --> "file3.txt (D)"
"""
        output = generate_mermaid_code(commit_info)
        self.assertEqual(output.strip(), expected_output.strip())

    @patch('builtins.open', new_callable=mock_open)
    def test_write_output(self, mock_file):
        write_output('/path/to/output', 'test content')
        mock_file().write.assert_called_once_with('test content')

    @patch('hw2.read_config')
    @patch('hw2.get_commit_tree')
    @patch('hw2.generate_mermaid_code')
    @patch('hw2.write_output')
    def test_main(self, mock_write_output, mock_generate_mermaid_code, mock_get_commit_tree, mock_read_config):
        mock_read_config.return_value = {
            'repo_path': '/path/to/repo',
            'output_path': '/path/to/output'
        }
        mock_get_commit_tree.return_value = {
            'abc123': {
                'message': 'Commit message 1',
                'children': [],
                'changes': ['A\tfile1.txt', 'M\tfile2.txt']
            },
            'abc456': {
                'message': 'Commit message 2',
                'children': [],
                'changes': ['D\tfile3.txt']
            }
        }
        mock_generate_mermaid_code.return_value = 'graph TD ...'

        main('dummy_config.xml')

        mock_read_config.assert_called_once_with('dummy_config.xml')
        mock_get_commit_tree.assert_called_once_with('/path/to/repo')
        mock_generate_mermaid_code.assert_called_once_with(mock_get_commit_tree.return_value)
        mock_write_output.assert_called_once_with('/path/to/output', 'graph TD ...')

if __name__ == '__main__':
    unittest.main()
