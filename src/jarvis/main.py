from rich.console import Console

from jarvis.core.app import JarvisApp

console = Console()


def banner():
    console.print("=" * 55, style="bold cyan")
    console.print("        JARVIS NEXT GENERATION", style="bold cyan")
    console.print("=" * 55, style="bold cyan")


def on_started():
    console.print("[bold green]✔ Event empfangen: app.started[/bold green]")


def main():
    banner()

    app = JarvisApp()

    app.events.subscribe("app.started", on_started)

    app.start()


if __name__ == "__main__":
    main()