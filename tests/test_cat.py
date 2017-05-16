import json

import pytest
import click.testing
from click import Command, Context
from mock import MagicMock

from jsoncat.cli import main
from jsoncat.core import load_json_files


D1 = {"asteroid": "433 Eros"}
D2 = {"asteroid": "951 Gaspra"}
J1 = json.dumps(D1)
J2 = json.dumps(D2)
JE = '{Invalid JSON'


@pytest.fixture
def runner():
    return click.testing.CliRunner()


def test_no_args_with_stdin(runner):
    result = runner.invoke(main, args=[], input=J1)
    assert result.exit_code == 0
    assert eval(result.output) == D1


def test_stdin_arg(runner):
    result = runner.invoke(main, args=['-'], input=J1)
    assert result.exit_code == 0
    assert eval(result.output) == D1


def test_single_filename(runner):
    with runner.isolated_filesystem():
        with open('t1.json', 'w') as f:
            f.write(J1)
        result = runner.invoke(main, args=['t1.json'])
        assert result.exit_code == 0
        assert eval(result.output) == D1


def test_stdin_arg_plus_filename(runner):
    with runner.isolated_filesystem():
        with open('t2.json', 'w') as f:
            f.write(J2)
        result = runner.invoke(main, args=['-', 't2.json'], input=J1)
        assert result.exit_code == 0
        assert eval(result.output) == [D1, D2]


def test_stdin_as_second_arg(runner):
    with runner.isolated_filesystem():
        with open('t1.json', 'w') as f:
            f.write(J1)
        result = runner.invoke(main, args=['t1.json', '-'], input=J2)
        assert result.exit_code == 0
        assert eval(result.output) == [D1, D2]


def test_two_filenames(runner):
    with runner.isolated_filesystem():
        with open('t1.json', 'w') as f:
            f.write(J1)
        with open('t2.json', 'w') as f:
            f.write(J2)
        result = runner.invoke(main, args=['t1.json', 't2.json'])
        assert result.exit_code == 0
        assert eval(result.output) == [D1, D2]


def test_two_filenames_reversed(runner):
    with runner.isolated_filesystem():
        with open('t1.json', 'w') as f:
            f.write(J1)
        with open('t2.json', 'w') as f:
            f.write(J2)
        result = runner.invoke(main, args=['t2.json', 't1.json'])
        assert result.exit_code == 0
        assert eval(result.output) == [D2, D1]


def test_indented_json(runner):
    result = runner.invoke(main, args=[], input=J1)
    assert result.exit_code == 0
    assert len(result.output.splitlines()) == 3


def test_compact_json(runner):
    result = runner.invoke(main, args=['--compact'], input=J1)
    assert result.exit_code == 0
    assert len(result.output.splitlines()) == 1


def test_json_decode_error(runner):
    result = runner.invoke(main, args=[], input=JE)
    assert result.exit_code == 1


def test_no_args_without_stdin(runner):
    result = runner.invoke(main, args=[])
    assert result.exit_code == 1


def test_no_args_with_no_stdin_and_is_tty():
    ctx = Context(Command('jsncat'))
    ctx.get_usage = MagicMock(return_value='Usage: jsncat ...')
    with pytest.raises(SystemExit):
        load_json_files(ctx=ctx, is_tty=True)
