"""The Janken package main!

"""

import argparse
import sys

from janken import predict


def get_parser() -> argparse.ArgumentParser:
    """Returns a parser for Janken!

    Returns:
        Argument parser for Janken.

    """

    parser = argparse.ArgumentParser(description='Interpret Janken images.')
    parser.add_argument('images', nargs='+', help='image files to interpret')
    return parser


def main():
    """Runs Janken! Tells you whether rock, paper, or scissors were thrown.

    """

    parser = get_parser()
    args = parser.parse_args()
    predict(args.images)


if __name__ == '__main__':
    sys.exit(main())
