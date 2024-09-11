import unittest
from src.arg_parser import parse_args
from src.config import Config


class TestArgParser(unittest.TestCase):

    def test_default_port(self):
        args = parse_args(['hostname', 'username'])
        self.assertEqual(args[1], Config.DEFAULT_PORT)
        self.assertFalse(args[3])

    def test_custom_port(self):
        args = parse_args(['-p', '12345', 'hostname', 'username'])
        self.assertEqual(args[1], 12345)
        self.assertFalse(args[3])

    def test_ssl_flag(self):
        args = parse_args(['-s', 'hostname', 'username'])
        self.assertEqual(args[1], Config.TLS_PORT)
        self.assertTrue(args[3])

    def test_ssl_flag_with_custom_port(self):
        args = parse_args(['-s', '-p', '12345', 'hostname', 'username'])
        self.assertEqual(args[1], 12345)
        self.assertTrue(args[3])

    def test_hostname_and_username(self):
        args = parse_args(['example.com', 'john.doe'])
        self.assertEqual(args[0], 'example.com')
        self.assertEqual(args[2], 'john.doe')


if __name__ == '__main__':
    unittest.main()
