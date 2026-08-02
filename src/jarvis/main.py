from rich.console import Console

from jarvis.core.app import JarvisApp

console = Console()


def banner():
    console.print("=" * 55, style="bold cyan")
    console.print("        JARVIS NEXT GENERATION", style="bold cyan")
    console.print("=" * 55, style="bold cyan")


def main():
    banner()

    app = JarvisApp()
    app.start()

    console.print()
    console.print("[bold green]JARVIS Kernel erfolgreich gestartet[/bold green]")


if __name__ == "__main__":
    main()