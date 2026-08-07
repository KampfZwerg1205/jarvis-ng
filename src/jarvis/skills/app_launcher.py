from __future__ import annotations

import os

from jarvis.skills.base import Skill
from jarvis.system.applications import ApplicationScanner


class AppLauncherSkill(Skill):
    """Startet installierte Programme."""

    def __init__(self) -> None:
        self.scanner = ApplicationScanner()

    @property
    def name(self) -> str:
        return "app_launcher"

    def can_handle(self, prompt: str) -> bool:
        prompt = prompt.lower().strip()

        commands = (
            "öffne ",
            "starte ",
            "launch ",
            "mach ",
        )

        return any(prompt.startswith(command) for command in commands)

    def confidence(self, prompt: str) -> float:
        if self.can_handle(prompt):
            return 0.8

        return 0.0

    def execute(self, prompt: str) -> str:
        application_name = self._extract_application_name(prompt)

        if not application_name:
            return "Ich konnte keine Anwendung erkennen."

        applications = self.scanner.scan()

        # Bekannte Synonyme
        aliases = {
            "vs code": "visual studio code",
            "vscode": "visual studio code",
            "chrome": "google chrome",
            "edge": "microsoft edge",
        }

        application_name = aliases.get(
            application_name,
            application_name,
        )

        # Exakte Übereinstimmung
        if application_name in applications:
            shortcut = applications[application_name]

            try:
                os.startfile(shortcut)
                return f"{application_name} wurde gestartet."
            except OSError:
                return f"{application_name} konnte nicht gestartet werden."

        # Teilübereinstimmung
        for app_name, shortcut in applications.items():
            if app_name in application_name:
                try:
                    os.startfile(shortcut)
                    return f"{app_name} wurde gestartet."
                except OSError:
                    return f"{app_name} konnte nicht gestartet werden."

        return f"Ich konnte die Anwendung '{application_name}' nicht finden."

    def _extract_application_name(self, prompt: str) -> str | None:
        """Entfernt den Sprachbefehl und gibt nur den App-Namen zurück."""

        text = prompt.lower().strip()

        commands = (
            "öffne ",
            "starte ",
            "launch ",
            "mach ",
        )

        # Sprachbefehl entfernen
        for command in commands:
            if text.startswith(command):
                text = text[len(command):]
                break

        text = text.strip()

        # Nachgestellte Befehlswörter entfernen
        endings = (
            " auf",
            " bitte",
        )

        changed = True

        while changed:
            changed = False

            for ending in endings:
                if text.endswith(ending):
                    text = text[:-len(ending)].strip()
                    changed = True

        # Artikel entfernen
        articles = (
            "den ",
            "die ",
            "das ",
            "der ",
        )

        for article in articles:
            if text.startswith(article):
                text = text[len(article):]
                break

        text = text.strip()

        return text if text else None