from rich import print

from jarvis.cli.app import app
from jarvis.main import main


@app.command()
def start() -> None:
    """Startet JARVIS."""
    main()


@app.command()
def version() -> None:
    """Zeigt die aktuelle Version an."""
    print("[cyan]JARVIS-NG[/cyan] 0.1.0-alpha.2")