"""The Janken package main!

"""

import sys

import gooey

from janken import predict


def get_target() -> str:
    """Returns an appropriate `target` argument for :func:`gooey.Gooey`.

    Returns:
       :func:`gooey.Gooey` `target` string.

    """

    import mimetypes
    import os
    from gooey.gui.util.quoting import quote

    run_cmd = sys.argv[0]

    # Run PyInstaller frozen executables as-is
    if hasattr(sys, 'frozen'):
        return quote(run_cmd)

    # Run Windows entry point launchers as-is
    if not os.path.exists(run_cmd) and os.path.exists(run_cmd + '.exe'):
        return quote(run_cmd + '.exe')

    # Run Linux/Unix entry points as-is
    if (not os.path.splitext(run_cmd)[1] and
        os.access(run_cmd, os.X_OK) and
        mimetypes.guess_type(run_cmd).startswith('text')):

        with open(run_cmd) as run_cmd_file:
            if 'sys.exit(load_entry_point' in run_cmd_file.read():
                return quote(run_cmd)

    # Default to Gooey run command
    return '{} -u {}'.format(quote(sys.executable), quote(run_cmd))


def get_parser() -> gooey.GooeyParser:
    """Returns a parser for Janken!

    Returns:
        Argument parser for Janken.

    """

    parser = gooey.GooeyParser(description='Interpret Janken images.')
    parser.add_argument(
        'images',
        nargs='+',
        help='image files to interpret',
        widget='MultiFileChooser',
    )
    return parser


@gooey.Gooey(
    target=get_target(),
    default_size=(960, 530),
    terminal_font_family=
        'Consolas' if sys.platform.startswith('win') else 'Lucida Sans Mono',
)
def main():
    """Runs Janken! Tells you whether rock, paper, or scissors were thrown.

    """

    parser = get_parser()
    args = parser.parse_args()
    predict(args.images)


if __name__ == '__main__':
    sys.exit(main())
