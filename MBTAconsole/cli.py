from typing import Optional

import typer

from MBTAconsole import __app_name__, __version__, MBTAconsole

app = typer.Typer()

@app.command()
def show_routes():
    MBTAconsole.get_long_names()

@app.command()
def longest_route():
    MBTAconsole.get_longest_route()

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return