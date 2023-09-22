from typer.testing import CliRunner

from MBTAconsole import __app_name__, __version__, cli

runner = CliRunner()

def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout

def test_show_route_ux():
    result = runner.invoke(cli.app, ["show-routes"])
    assert result.exit_code == 0
    assert "Red Line" in result.stdout

def test_longest_route_ux():
    result = runner.invoke(cli.app, ["longest-route"])
    assert result.exit_code == 0
    assert "Green Line" in result.stdout