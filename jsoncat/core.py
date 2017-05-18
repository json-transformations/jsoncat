import json
import sys

import click


def output_lines(lines, color=None, err=False):
    """"Write a sequence of lines to standard out or standard error.

   When writing data to standard output or standard error if a SIGINT
   ("program interrupt") signal is sent the KeyboardInterrupError
   message and stack trace will be suppressed; this makes a nice clean
   break when the user types the INTR character; normally Ctrl-c.
    """
    try:
        for line in lines:
            click.echo(line, color=color, err=err)
    except KeyboardInterrupt:
        err = True

    if err:
        sys.exit(1)


def output_text(text, color=None, err=False):
    """Send text to standard out or standard error w/ SIGINT wrapper."""
    output_lines([text], color=color, err=err)


def load_json(filename):
    with click.open_file(filename) as file_:
        return json.load(file_)


def load_json_files(*filenames, **kwds):
    """JSON Decoder with Standard Input/File Handler.

    Args:
        filenames [str, ...]:
            A list of filenames to concatenate.

    Kwds:
        ctx (click.Context):
            Command Context (used to display command usage message).

        is_tty:
            Set to True if the STDIN is connected to a TTY(-like)
            device; typically set to sys.stdin.isatty()

    Returns:
        The JSON document as a dictionary.

    +---------+-------------------+--------------------------------+
    | Stdin   | File Name(s)      | Defined Behavior               |
    +=========+===================+================================+
    | No Data | No Filename       | Print command usage message    |
    +---------+-------------------+--------------------------------+
    | Data    | No Filename       | Read JSON data from STDIN      |
    +---------+-------------------+--------------------------------+
    | Data    | Dash char. (-)    | Read JSON data from STDIN      |
    +---------+-------------------+--------------------------------+
    | No Data | Dash char. (-)    | Accept user input until EOF    |
    +---------+-------------------+--------------------------------+
    | Either  | Filename          | Read JSON data from file       |
    +---------+-------------------+--------------------------------+
    | Either  | File1, File2, ... | Concatenate JSON data in array |
    +---------+-------------------+--------------------------------+
    """
    if not filenames:
        if kwds.get('is_tty'):
            ctx = kwds.get('ctx', None)
            if ctx:
                output_text(ctx.get_usage())
            usage = "Try `{cmd} --help' for more information."
            output_text(usage.format(cmd='jsncat'))
            sys.exit(1)
        else:
            filenames = ['-']
    try:
        result = [load_json(f) for f in filenames]
    except (EnvironmentError, ValueError) as e:
        output_text(e, err=True)
        sys.exit(1)
    return result[0] if len(filenames) == 1 else result


def dump_json(output, compact=False):
    """Format JSON; compact/squeezed or indented w/ sorted keys."""
    if compact:
        indent = None
        separators = (',', ':')
        sort_keys = False
    else:
        indent = 2
        separators = None
        sort_keys = True
    return json.dumps(output, indent=indent, separators=separators,
                      sort_keys=sort_keys)
