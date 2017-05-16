import click
import sys

from . import __version__
from .core import load_json_files, dump_json, output_text


@click.command()
@click.argument('jsonfiles', nargs=-1, type=click.Path(readable=True))
@click.option('-c', '--compact', is_flag=True,
              help='Compact (squeeze) JSON.')
@click.version_option(version=__version__, prog_name='jsncat')
@click.pass_context
def main(ctx, jsonfiles, compact):
    """Concatenate JSON FILE(s), or standard input, to standard output."""
    json_dict = load_json_files(*jsonfiles, ctx=ctx, is_tty=sys.stdin.isatty())
    json_data = dump_json(json_dict, compact=compact)
    output_text(json_data)


if __name__ == '__main__':
    main()
