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
            # -----------------------------------------------------
            # NOTEPAD / EDITOR
            # -----------------------------------------------------

            "öffne notepad",
            "öffne den notepad",
            "starte notepad",
            "starte den notepad",

            "öffne editor",
            "öffne den editor",
            "starte editor",
            "starte den editor",

            # -----------------------------------------------------
            # TASCHENRECHNER
            # -----------------------------------------------------

            "öffne taschenrechner",
            "öffne den taschenrechner",
            "starte taschenrechner",
            "starte den taschenrechner",

            "öffne rechner",
            "öffne den rechner",
            "starte rechner",
            "starte den rechner",

            # -----------------------------------------------------
            # HERUNTERFAHREN
            # -----------------------------------------------------

            "fahre meinen pc herunter",
            "fahr meinen pc herunter",
            "fahre den pc herunter",
            "fahr den pc herunter",

            "pc herunterfahren",
            "computer herunterfahren",
            "herunterfahren",

            # -----------------------------------------------------
            # NEUSTART
            # -----------------------------------------------------

            "starte meinen pc neu",
            "starte den pc neu",

            "pc neu starten",
            "computer neu starten",

            "neustart",
            "neu starten",

            # -----------------------------------------------------
            # PC SPERREN
            # -----------------------------------------------------

            "sperre meinen pc",
            "sperre den pc",

            "pc sperren",
            "computer sperren",

            "sperren",
        )

        return any(command in prompt for command in commands)

    def confidence(self, prompt: str) -> float:
        if self.can_handle(prompt):
            return 1.0

        return 0.0

    def execute(self, prompt: str) -> str:
        prompt = prompt.lower().strip()

        # ---------------------------------------------------------
        # NOTEPAD / EDITOR
        # ---------------------------------------------------------

        if "notepad" in prompt or "editor" in prompt:
            if SystemActions.open_notepad():
                return "Notepad wurde geöffnet."

            return "Notepad konnte nicht gestartet werden."

        # ---------------------------------------------------------
        # TASCHENRECHNER
        # ---------------------------------------------------------

        if (
            "taschenrechner" in prompt
            or "rechner" in prompt
        ):
            if SystemActions.open_calculator():
                return "Der Taschenrechner wurde geöffnet."

            return "Der Taschenrechner konnte nicht gestartet werden."

        # ---------------------------------------------------------
        # HERUNTERFAHREN
        # ---------------------------------------------------------

        if (
            "herunterfahren" in prompt
            or "fahre meinen pc herunter" in prompt
            or "fahr meinen pc herunter" in prompt
            or "fahre den pc herunter" in prompt
            or "fahr den pc herunter" in prompt
            or "herunter" in prompt
        ):
            return (
                "Das Herunterfahren wurde erkannt. "
                "Eine Sicherheitsbestätigung wird benötigt."
            )

        # ---------------------------------------------------------
        # NEUSTART
        # ---------------------------------------------------------

        if (
            "neu starten" in prompt
            or "neustart" in prompt
            or "starte meinen pc neu" in prompt
            or "starte den pc neu" in prompt
        ):
            return (
                "Der Neustart wurde erkannt. "
                "Eine Sicherheitsbestätigung wird benötigt."
            )

        # ---------------------------------------------------------
        # PC SPERREN
        # ---------------------------------------------------------

        if (
            "sperre meinen pc" in prompt
            or "sperre den pc" in prompt
            or "pc sperren" in prompt
            or "computer sperren" in prompt
            or prompt == "sperren"
        ):
            return (
                "Die PC-Sperre wurde erkannt. "
                "Die eigentliche Aktion wird später über "
                "eine Sicherheitsbestätigung ausgeführt."
            )

        # ---------------------------------------------------------
        # FALLBACK
        # ---------------------------------------------------------

        return "Diese Systemaktion wird noch nicht unterstützt."