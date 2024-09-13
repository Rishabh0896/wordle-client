import argparse
from typing import Tuple

from src.config import Config


def parse_args(args: list) -> Tuple[str, int, str, bool]:
    """
    Parse command-line arguments for the Wordle client program.

    This function sets up an argument parser to handle the following arguments:
    - hostname: (required) The hostname of the server to connect to.
    - username: (required) The Northeastern username for authentication.
    - -p: (optional) The TCP port the server is listening on.
    - -s: (optional) A flag to use TLS encrypted socket connection.

    Args:
        args (list): List of command-line arguments to parse.

    Returns:
        Tuple[str, int, str, bool]: A tuple containing:
            - hostname (str): The server hostname.
            - port (int): The port number to connect to.
            - username (str): The Northeastern username.
            - use_tls (bool): Whether to use TLS encryption.
    """
    parser = argparse.ArgumentParser(description="Client program to connect to a server.")

    # Add optional arguments
    parser.add_argument('-p', type=int, help="tcp port the server is listening on", default=Config.DEFAULT_PORT)
    parser.add_argument('-s', action='store_true', help="use TLS encrypted socket connection")

    # Add required positional arguments
    parser.add_argument('hostname', type=str, help="hostname of the server")
    parser.add_argument('username', type=str, help="northeastern username")

    # Parse the arguments
    parsed_args = parser.parse_args(args)

    # If TLS is enabled and no port is specified, use TLS port
    if parsed_args.s:
        if parsed_args.p == Config.DEFAULT_PORT:
            parsed_args.p = Config.TLS_PORT

    return parsed_args.hostname, parsed_args.p, parsed_args.username, parsed_args.s
