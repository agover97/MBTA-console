from typer.testing import CliRunner

from MBTAconsole import __app_name__, __version__, cli

runner = CliRunner()

def test_version():
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout

def test_show_route_cli():
    result = runner.invoke(cli.app, ["show-routes"])
    assert result.exit_code == 0
    assert "Red Line" in result.stdout

def test_longest_route_cli():
    result = runner.invoke(cli.app, ["longest-route"])
    assert result.exit_code == 0
    assert "Green Line" in result.stdout

def test_shortest_route_cli():
    result = runner.invoke(cli.app, ["shortest-route"])
    assert result.exit_code == 0
    assert "Mattapan Trolley" in result.stdout

def test_connecting_stops_cli():
    result = runner.invoke(cli.app, ["connecting-stops"])
    assert result.exit_code == 0
    assert "Arlington" in result.output
    assert "Ashmont" in result.output
    assert "Boylston" in result.output
    assert "Copley" in result.output
    assert "Downtown Crossing" in result.output
    assert "Government Center" in result.output
    assert "Haymarket" in result.output
    assert "Hynes Convention Center" in result.output
    assert "Kenmore" in result.output
    assert "Lechmere" in result.output
    assert "North Station" in result.output
    assert "Park Street" in result.output
    assert "Science Park/West End" in result.output
    assert "State" in result.output

def test_find_route():
    result = runner.invoke(cli.app, ["find-route", "Braintree", "Arlington"])
    assert result.exit_code == 0
    assert "Red Line, Green Line" in result.stdout
    