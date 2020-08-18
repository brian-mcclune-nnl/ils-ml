"""The Janken package main!

"""

import sys

from janken import predict


def main():
    """Runs Janken! Tells you whether rock, paper, or scissors were thrown.

    """

    predict(sys.argv[1:])


if __name__ == '__main__':
    sys.exit(main())