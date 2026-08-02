from rich.console import Console

console = Console()


def banner() -> None:
    console.print("=" * 50, style="bold cyan")
    console.print("        JARVIS NEXT GENERATION", style="bold cyan")
    console.print("=" * 50, style="bold cyan")


def main() -> None:
    banner()
    console.print("[green]✓ Kernel gestartet[/green]")
    console.print("[green]✓ Foundation geladen[/green]")
    console.print("[green]✓ Version 0.1.0[/green]")
    console.print()
    console.print("[bold cyan]Willkommen bei JARVIS-NG[/bold cyan]")