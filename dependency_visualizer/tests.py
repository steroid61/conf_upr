import unittest
from unittest.mock import patch, MagicMock
from visualizer import (
    read_object,
    parse_commit,
    CommitNode,
    build_commit_graph,
    generate_dot
)


class TestGitCommitVisualizer(unittest.TestCase):

    @patch('subprocess.run')
    def test_read_object(self, mock_run):
        # Настройка
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout='tree 123456\nparent abcdef\n', stderr=''),  # git cat-file
            MagicMock(returncode=0, stdout='commit', stderr='')  # git cat-file -t
        ]

        sha1 = 'abc123'
        obj = read_object('/Users/timofey/Desktop/конф_упр/my_rep', sha1)

        # Проверка
        self.assertEqual(obj.sha1, sha1)
        self.assertEqual(obj.content, 'tree 123456\nparent abcdef\n')

    @patch('git.Repo')
    def test_parse_commit(self, mock_repo):
        # Подготовка мока репозитория
        mock_commit = MagicMock()
        mock_commit.stats.files = {'file1.txt': {}, 'file2.txt': {}}

        # Настройка
        mock_repo.return_value.commit.return_value = mock_commit

        commit_content = (
            "tree 123456\n"
            "parent abcdef\n"
            "author John Doe <john@example.com> 1610000000 +0000\n"
            "\n"
            "Initial commit\n"
        )
        obj = MagicMock()
        obj.content = commit_content
        obj.sha1 = 'abc123'

        commit_node = parse_commit(obj, '/Users/timofey/Desktop/конф_упр/my_rep')

        # Проверка
        self.assertEqual(commit_node.author, 'John Doe <john@example.com>')
        self.assertIn('file1.txt', commit_node.files)
        self.assertIn('file2.txt', commit_node.files)

    @patch('git.Repo')
    @patch('visualizer.read_object')
    def test_build_commit_graph(self, mock_read_object, mock_repo):
        # Настройка мока репозитория
        mock_commit = MagicMock()
        mock_commit.hexsha = 'abc123'
        mock_commit.stats.files = {'file1.txt': {}, 'file2.txt': {}}

        mock_repo.return_value.iter_commits.return_value = [mock_commit]

        obj = MagicMock()
        obj.sha1 = 'abc123'
        obj.content = 'tree ...'

        mock_read_object.return_value = obj

        # Настройка возвращаемого значения parse_commit
        mock_commit_node = CommitNode(sha1='abc123', author='John Doe <john@example.com>', parents=[],
                                      files=['file1.txt', 'file2.txt'])
        mock_read_object.return_value = obj

        with patch('visualizer.parse_commit', return_value=mock_commit_node):
            graph = build_commit_graph('/Users/timofey/Desktop/конф_упр/my_rep', 'file1.txt')

        # Проверка
        self.assertIn('abc123', graph)
        self.assertEqual(len(graph), 1)
        self.assertIn('file1.txt', graph['abc123'].files)  # Проверка на наличие файла

    def test_generate_dot(self):
        # Подготовка графа
        node = CommitNode(
            sha1='abc123',
            author='John Doe <john@example.com>',
            parents=['abcdef'],
            files=['file1.txt', 'file2.txt']
        )
        graph = {'abc123': node}
        dot_output = generate_dot(graph)

        # Проверка формата вывода
        self.assertIn('digraph G {', dot_output)
        self.assertIn('abc123', dot_output)
        self.assertIn('John Doe <john@example.com>', dot_output)
        self.assertIn('Files: file1.txt, file2.txt', dot_output)


if __name__ == '__main__':
    unittest.main()
