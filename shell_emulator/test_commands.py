import unittest
from unittest.mock import patch
from emulator import ShellEmulator
import os

class TestShellEmulatorCommands(unittest.TestCase):
    def setUp(self):
        self.emulator = ShellEmulator('config.xml')

    def test_ls(self):
        with patch('builtins.print') as mock_print:
            self.emulator.ls()
            mock_print.assert_any_call('hello')
            mock_print.assert_any_call('my_folder')

    def test_cd_valid(self):
        self.emulator.cd('hello/documents')
        self.assertEqual(self.emulator.current_path, '/hello/documents')

    def test_cd_invalid(self):
        with patch('builtins.print') as mock_print:
            self.emulator.cd('hello/nonexistent_directory')
            self.assertEqual(self.emulator.current_path, '/')
            mock_print.assert_called_once_with('No such directory: hello/nonexistent_directory')

    def test_cp_file(self):
        self.emulator.cd('hello/documents')
        self.emulator.cp('file.txt', 'vfs/my_folder')
        self.assertTrue(os.path.isfile('vfs/my_folder/file.txt'))
        os.remove('vfs/my_folder/file.txt')

    def test_cp_file_not_found(self):
        with patch('builtins.print') as mock_print:
            self.emulator.cd('hello/documents')
            self.emulator.cp('nonexistent.txt', 'destination.txt')
            mock_print.assert_called_once_with('No such file: nonexistent.txt')

    def test_date(self):
        with patch('builtins.print') as mock_print:
            self.emulator.date()
            mock_print.assert_called_once()

    if __name__ == '__main__':
        unittest.main()