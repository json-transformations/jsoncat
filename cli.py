import json
import sys

import click
import click._termui_impl
if sys.version_info.major == '2':
    from contextlib2 import suppress
else:
    from contextlib import suppress

__version__ = '0.8'


class JSONFile(click.File):
    name = 'JSON.load'

    def __init__(self, **kwds):
        super(JSONFile, self).__init__(**kwds)

    def convert(self, value, param, ctx):
        self.encoding = ctx.params['encoding']
        if value == '-' and click._termui_impl.isatty(sys.stdin):
            return self.display_usage(param, ctx)
        try:
            f = super(JSONFile, self).convert(value, param, ctx)
            return json.load(f)
        except (json.JSONDecodeError, TypeError) as e:
            mesg = '{filename} does not contain valid JSON: {error_mesg}'
            self.failed(mesg, e, value, param, ctx)
        except UnicodeError as e:
            filename = click._compat.filename_to_ui(value)
            error_mesg = click._compat.get_streerror(e)
            output = '{}: {}'.format(filename, error_mesg)
            click.echo(output, err=True)
            sys.exit(1)
        except LookupError as e:
            error_mesg = click._compat.get_streerror(e)
            click.echo(error_mesg, err=True)
            sys.exit(1)
        return

    def display_usage(self, param, ctx):
        click.echo(ctx.get_usage())
        help_mesg = "Try `{cmd_name} --help' for more information."
        click.echo(help_mesg.format(cmd_name=ctx.command.name), err=True)
        sys.exit(1)

    def failed(self, mesg, err, value, param, ctx):
        filename = click._compat.filename_to_ui(value)
        error_mesg = click._compat.get_streerror(err)
        output = mesg.format(filename=filename, error_mesg=error_mesg)
        self.fail(output, param, ctx)


def json_dump_settings(ctx, param, value):
    indent = int(value)
    return {
        "indent": indent or None,
        "separators": None if indent else (',', ':'),
        "sort_keys": bool(indent)
    }


jsonfile_arg = click.argument(
    'jsonfile', type=JSONFile(), default='-'
)
jsonfiles_arg = click.argument(
    'jsonfiles', nargs=-1, type=JSONFile(), metavar='...'
)
encoding_option = click.option(
    '-e', '--encoding',
    required=False, is_eager=True
)
indent_option = click.option(
    '-i', '--indent',
    type=click.Choice(['0', '2', '4']), default='2',
    callback=json_dump_settings,
    help='Indent size (default=2); if zero output is compacted (squeezed.)'
)


@click.command()
@jsonfile_arg
@jsonfiles_arg
@encoding_option
@indent_option
@click.version_option()
@click.pass_context
def jsoncat(ctx, jsonfile, jsonfiles, encoding, indent):
    """Concatenate JSON FILE(s), or standard input & format standard output."""
    with suppress(KeyboardInterrupt):
        data = (jsonfile,) + jsonfiles if jsonfiles else jsonfile
        print(json.dumps(data, **indent))


if __name__ == '__main__':
    jsoncat()
