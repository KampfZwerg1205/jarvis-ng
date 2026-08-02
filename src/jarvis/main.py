from rich.console import Console

from jarvis.core.app import JarvisApp

console = Console()


def banner() -> None:
    console.print("=" * 50, style="bold cyan")
    console.print("        JARVIS NEXT GENERATION", style="bold cyan")
    console.print("=" * 50, style="bold cyan")


def main() -> None:
    banner()

    app = JarvisApp()
    app.start()

    console.print()
    console.print("[bold green]JARVIS Kernel erfolgreich gestartet[/bold green]")