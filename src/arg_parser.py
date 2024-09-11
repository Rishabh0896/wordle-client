import argparse

from src.config import Config


def parse_args(args=None):
    parser = argparse.ArgumentParser(description="Client program to connect to a server.")

    # Add optional arguments
    # If the port argument is not provided assume that the port is a non TLS port
    parser.add_argument('-p', type=int, help="tcp port the server is listening on", default=Config.DEFAULT_PORT)
    parser.add_argument('-s', action='store_true', help="use TLS encrypted socket connection")

    # Add required positional arguments
    parser.add_argument('hostname', type=str, help="hostname of the server")
    parser.add_argument('username', type=str, help="northeastern username")

    # Parse the arguments
    args = parser.parse_args(args)

    # Logic for choosing ports based on TLS flag
    if args.s:
        # If TLS is enabled and no port is specified, use TLS port
        if args.p == Config.DEFAULT_PORT:
            args.p = Config.TLS_PORT



