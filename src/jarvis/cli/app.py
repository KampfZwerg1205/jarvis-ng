import typer

app = typer.Typer(
    name="jarvis",
    help="JARVIS Next Generation Command Line Interface",
    no_args_is_help=True,
)

from jarvis.cli import commands
from jarvis.cli import chat