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
            # Anwendungen
            "öffne ",
            "starte ",
            "mach auf ",

            # PC sperren
            "sperre meinen pc",
            "sperr meinen pc",
            "sperre den pc",
            "sperr den pc",

            # Herunterfahren
            "fahre meinen pc herunter",
            "fahr meinen pc herunter",
            "fahre den pc herunter",
            "fahr den pc herunter",
            "fahre meinen computer herunter",
            "fahr meinen computer herunter",
            "pc herunterfahren",
            "computer herunterfahren",
            "herunterfahren",

            # Neustart
            "starte meinen pc neu",
            "starte den pc neu",
            "starte meinen computer neu",
            "starte den computer neu",
            "pc neu starten",
            "computer neu starten",
            "pc neustarten",
            "computer neustarten",

            # Einstellungen
            "öffne die einstellungen",
            "öffne einstellungen",
        )

        return any(command in prompt for command in commands)

    def confidence(self, prompt: str) -> float:
        if self.can_handle(prompt):
            return 1.0

        return 0.0

    def execute(self, prompt: str) -> str:
        prompt = prompt.lower().strip()

        # ---------------------------------------------------------
        # PC sperren
        # ---------------------------------------------------------

        if (
            "sperre meinen pc" in prompt
            or "sperr meinen pc" in prompt
            or "sperre den pc" in prompt
            or "sperr den pc" in prompt
        ):
            return (
                "Die PC-Sperre ist erkannt. "
                "Die eigentliche Aktion wird später über eine "
                "Sicherheitsbestätigung ausgeführt."
            )

        # ---------------------------------------------------------
        # Herunterfahren
        # ---------------------------------------------------------

        if (
            "fahre meinen pc herunter" in prompt
            or "fahr meinen pc herunter" in prompt
            or "fahre den pc herunter" in prompt
            or "fahr den pc herunter" in prompt
            or "fahre meinen computer herunter" in prompt
            or "fahr meinen computer herunter" in prompt
            or "pc herunterfahren" in prompt
            or "computer herunterfahren" in prompt
            or prompt == "herunterfahren"
        ):
            return (
                "Das Herunterfahren wurde erkannt. "
                "Eine Sicherheitsbestätigung wird benötigt."
            )

        # ---------------------------------------------------------
        # Neustart
        # ---------------------------------------------------------

        if (
            "starte meinen pc neu" in prompt
            or "starte den pc neu" in prompt
            or "starte meinen computer neu" in prompt
            or "starte den computer neu" in prompt
            or "pc neu starten" in prompt
            or "computer neu starten" in prompt
            or "pc neustarten" in prompt
            or "computer neustarten" in prompt
        ):
            return (
                "Der Neustart wurde erkannt. "
                "Eine Sicherheitsbestätigung wird benötigt."
            )

        # ---------------------------------------------------------
        # Windows-Einstellungen
        # ---------------------------------------------------------

        if (
            "öffne die einstellungen" in prompt
            or "öffne einstellungen" in prompt
        ):
            if SystemActions.open_settings():
                return "Die Windows-Einstellungen wurden geöffnet."

            return "Die Windows-Einstellungen konnten nicht geöffnet werden."

        # ---------------------------------------------------------
        # Notepad
        # ---------------------------------------------------------

        if "notepad" in prompt or "editor" in prompt:
            if SystemActions.open_notepad():
                return "Notepad wurde geöffnet."

            return "Notepad konnte nicht gestartet werden."

        # ---------------------------------------------------------
        # Taschenrechner
        # ---------------------------------------------------------

        if "taschenrechner" in prompt or "rechner" in prompt:
            if SystemActions.open_calculator():
                return "Der Taschenrechner wurde geöffnet."

            return "Der Taschenrechner konnte nicht gestartet werden."

        # ---------------------------------------------------------
        # Bekannte App-Synonyme
        # ---------------------------------------------------------

        aliases = {
            "vs code": "visual studio code",
            "vscode": "visual studio code",
            "chrome": "google chrome",
            "edge": "microsoft edge",
        }

        application_name = None

        for alias, real_name in aliases.items():
            if alias in prompt:
                application_name = real_name
                break

        # ---------------------------------------------------------
        # Installierte Anwendungen
        # ---------------------------------------------------------

        if application_name is None:
            for name in self.applications:
                if name.lower() in prompt:
                    application_name = name
                    break

        if application_name is not None:
            path = self.applications.get(application_name)

            if path and SystemActions.open_application(path):
                return f"{application_name} wurde gestartet."

            return f"{application_name} konnte nicht gestartet werden."

        return "Ich konnte diese Systemaktion nicht finden."