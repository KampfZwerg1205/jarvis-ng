from rich.console import Console

from jarvis.core.app import JarvisApp

console = Console()


def banner() -> None:
    console.print("=" * 55, style="bold cyan")
    console.print("        JARVIS NEXT GENERATION", style="bold cyan")
    console.print("=" * 55, style="bold cyan")


def on_started() -> None:
    console.print("[bold green]✓ Event erhalten: app.started[/bold green]")


def main() -> None:
    banner()

    app = JarvisApp()

    app.events.subscribe("app.started", on_started)

    app.start()


if __name__ == "__main__":
    main()