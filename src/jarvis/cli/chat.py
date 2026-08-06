from rich.console import Console

from jarvis.ai.providers import GeminiProvider
from jarvis.ai.router import AIRouter
from jarvis.cli.app import app
from jarvis.conversation.manager import ConversationManager

console = Console()


@app.command()
def chat() -> None:
    """Startet den interaktiven Chat."""

    console.print("=" * 55, style="bold cyan")
    console.print("        JARVIS NEXT GENERATION", style="bold cyan")
    console.print("=" * 55, style="bold cyan")

    console.print("\n[green]JARVIS ist bereit.[/green]")
    console.print("[dim]Tippe 'exit' zum Beenden.[/dim]\n")

    router = AIRouter()
    router.register(GeminiProvider())

    conversation = ConversationManager(router)

    while True:
        prompt = input("Du: ")

        if prompt.lower() in ("exit", "quit"):
            console.print("\n[cyan]JARVIS beendet.[/cyan]")
            break

        try:
            answer = conversation.chat(prompt)
            console.print(f"[yellow]JARVIS:[/yellow] {answer}")
        except Exception as exc:
            console.print(f"[bold red]Fehler:[/bold red] {exc}")