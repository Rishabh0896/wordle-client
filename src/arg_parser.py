import argparse

from src.config import Config


def parse_args(args=None):
    parser = argparse.ArgumentParser(description="Client program to connect to a server.")

    # Add optional arguments
    parser.add_argument('-p', type=int, help="tcp port the server is listening on", default=Config.get_port())
    parser.add_argument('-s', action='store_true', help="use TLS encrypted socket connection")

    # Add required positional arguments
    parser.add_argument('hostname', type=str, help="hostname of the server")
    parser.add_argument('username', type=str, help="northeastern username")

    # Parse the arguments
    return parser.parse_args(args)
