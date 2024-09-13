import unittest
from src.arg_parser import parse_args
from src.config import Config


class TestArgParser(unittest.TestCase):
    """
    A test suite for the argument parser used in the Wordle client.

    This class contains unit tests to ensure that the argument parser
    correctly handles various command-line input scenarios.
    """

    def test_default_port(self):
        """
        Test if the default port is correctly set when no port is specified.

        This test checks if the parser returns the default port from the Config
        and sets the SSL flag to False when only when the port is not provided.
        """
        args = parse_args(['hostname', 'username'])
        self.assertEqual(args[1], Config.DEFAULT_PORT)
        self.assertFalse(args[3])

    def test_custom_port(self):
        """
        Test if a custom port is correctly parsed when specified.

        This test checks if the parser correctly sets the port to the custom value
        and keeps the SSL flag as False when a port is explicitly provided.
        """
        args = parse_args(['-p', '12345', 'hostname', 'username'])
        self.assertEqual(args[1], 12345)
        self.assertFalse(args[3])

    def test_ssl_flag(self):
        """
        Test if the SSL flag is correctly set when the -s option is used.

        This test checks if the parser sets the port to the TLS_PORT from Config
        and sets the SSL flag to True when the -s option is provided.
        """
        args = parse_args(['-s', 'hostname', 'username'])
        self.assertEqual(args[1], Config.TLS_PORT)
        self.assertTrue(args[3])

    def test_ssl_flag_with_custom_port(self):
        """
        Test if both SSL flag and custom port are correctly handled when specified together.

        This test checks if the parser correctly sets both the custom port and the SSL flag
        when both options are provided in the command-line arguments.
        """
        args = parse_args(['-s', '-p', '12345', 'hostname', 'username'])
        self.assertEqual(args[1], 12345)
        self.assertTrue(args[3])

    def test_hostname_and_username(self):
        """
        Test if hostname and username are correctly parsed when provided.

        This test checks if the parser correctly extracts and returns the hostname
        and username from the command-line arguments.
        """
        args = parse_args(['example.com', 'john.doe'])
        self.assertEqual(args[0], 'example.com')
        self.assertEqual(args[2], 'john.doe')


if __name__ == '__main__':
    unittest.main()
