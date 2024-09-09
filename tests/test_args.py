from argparse import ArgumentParser

from client import parse_args


def test_parser():
    # Add tests to check all scenarios of command line parsing. This medium article will help :
    # https://medium.com/programmers-journey/dead-simple-pytest-and-argparse-d1dbb6affbc3
    parser = parse_args(['-l', '-m'])