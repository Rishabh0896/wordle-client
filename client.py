#!/usr/bin/env python3

import argparse
import sys

from src.MySocket import MySocket

# Define default port constants
DEFAULT_PORT = 27993
TLS_PORT = 27994


def parse_args(args=None):
    parser = argparse.ArgumentParser(description="Client program to connect to a server.")

    # Add optional arguments
    parser.add_argument('-p', type=int, help="tcp port the server is listening on", default=DEFAULT_PORT)
    parser.add_argument('-s', action='store_true', help="use TLS encrypted socket connection")

    # Add required positional arguments
    parser.add_argument('hostname', type=str, help="hostname of the server")
    parser.add_argument('username', type=str, help="northeastern username")

    # Parse the arguments
    return parser.parse_args(args)


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    sock = MySocket()
    try:
        sock.connect(host=args.hostname, port=args.p)
        print(f"Connected to {args.hostname} on port {args.p} as {args.username}")
        # Figure about how to create and receive json messages
        # Figure out how the optimal strategy to win the game
        #
    except Exception as e:
        print(f"Failed to connect to {args.hostname} on port {args.p}: {e}")
