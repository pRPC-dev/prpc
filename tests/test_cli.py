from typer.testing import CliRunner
from prpc.cli import app

runner = CliRunner()

def test_hello():
    result = runner.invoke(app, ["hello", "--name", "Test"])
    assert result.exit_code == 0
    assert "Hello Test!" in result.stdout

def test_version():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "prpc version:" in result.stdout
