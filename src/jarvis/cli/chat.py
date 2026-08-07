from rich.console import Console

from jarvis.ai.providers import OllamaProvider
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
    console.print(
        "[dim]Befehle: /clear, /history, /exit[/dim]\n"
    )

    router = AIRouter()
    router.register(GeminiProvider())
    router.register(OllamaProvider())

    conversation = ConversationManager(router)

    while True:
        prompt = input("Du: ")

        if prompt.lower() in ("exit", "quit", "/exit"):
            console.print("\n[cyan]JARVIS beendet.[/cyan]")
            break

        if prompt.lower() == "/clear":
            conversation.history.clear()
            console.print(
                "[green]✓ Gesprächsverlauf gelöscht.[/green]"
            )
            continue

        if prompt.lower() == "/history":
            history = conversation.history.as_text()

            if history:
                console.print("\n[cyan]Gesprächsverlauf:[/cyan]")
                console.print(history)
                console.print()
            else:
                console.print(
                    "[dim]Noch kein Gesprächsverlauf vorhanden.[/dim]"
                )

            continue

        try:
            answer = conversation.chat(prompt)
            console.print(f"[yellow]JARVIS:[/yellow] {answer}")

        except Exception as exc:
            console.print(
                f"[bold red]Fehler:[/bold red] {exc}"
            )