from __future__ import annotations

from jarvis.skills.base import Skill
from jarvis.system.actions import SystemActions
from jarvis.system.applications import ApplicationScanner


class SystemActionSkill(Skill):
    """Führt sichere, vordefinierte Systemaktionen aus."""

    def __init__(self) -> None:
        self.scanner = ApplicationScanner()
        self.applications = self.scanner.scan()

    @property
    def name(self) -> str:
        return "system_actions"

    def can_handle(self, prompt: str) -> bool:
        prompt = prompt.lower().strip()

        commands = (
            "öffne ",
            "starte ",
            "mach auf ",
        )

        return any(command in prompt for command in commands)

    def confidence(self, prompt: str) -> float:
        if self.can_handle(prompt):
            return 1.0

        return 0.0

    def execute(self, prompt: str) -> str:
        prompt = prompt.lower().strip()

        # Notepad
        if "notepad" in prompt or "editor" in prompt:
            if SystemActions.open_notepad():
                return "Notepad wurde geöffnet."

            return "Notepad konnte nicht gestartet werden."

        # Taschenrechner
        if "taschenrechner" in prompt or "rechner" in prompt:
            if SystemActions.open_calculator():
                return "Der Taschenrechner wurde gestartet."

            return "Der Taschenrechner konnte nicht gestartet werden."

        # Bekannte Synonyme
        aliases = {
            "vs code": "visual studio code",
            "vscode": "visual studio code",
            "visual studio code": "visual studio code",
            "steam": "steam",
            "spotify": "spotify",
            "firefox": "firefox",
            "discord": "discord",
            "chrome": "google chrome",
            "edge": "microsoft edge",
        }

        # Alias auflösen
        application_name = None

        for alias, real_name in aliases.items():
            if alias in prompt:
                application_name = real_name
                break

        # Wenn kein Alias gefunden wurde,
        # direkt nach App-Namen suchen
        if application_name is None:
            for name in self.applications:
                if name.lower() in prompt:
                    application_name = name
                    break

        # Anwendung starten
        if application_name is not None:
            path = self.applications.get(application_name)

            if path and SystemActions.open_application(path):
                return f"{application_name} wurde gestartet."

            return f"{application_name} konnte nicht gestartet werden."

        return "Ich konnte diese Anwendung nicht finden."