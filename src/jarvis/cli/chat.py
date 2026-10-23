from rich.console import Console

from jarvis.ai.providers import GeminiProvider, OllamaProvider
from jarvis.ai.router import AIRouter
from jarvis.cli.app import app
from jarvis.conversation.manager import ConversationManager
from jarvis.core.config import settings

console = Console()


def create_ai_router() -> AIRouter:
    """Erstellt einen Router, der standardmäßig lokal über Ollama arbeitet."""

    router = AIRouter()
    router.register(OllamaProvider())

    if settings.ai_provider == "gemini" and settings.gemini_api_key:
        router.register(GeminiProvider())

    return router


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

    conversation = ConversationManager(create_ai_router())

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
