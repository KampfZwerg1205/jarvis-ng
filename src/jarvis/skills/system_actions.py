from __future__ import annotations

from jarvis.skills.base import Skill
from jarvis.system.actions import SystemActions


class SystemActionSkill(Skill):
    """Führt sichere, vordefinierte Systemaktionen aus."""

    @property
    def name(self) -> str:
        return "system_actions"

    def can_handle(self, prompt: str) -> bool:
        prompt = prompt.lower().strip()

        commands = (
            # -------------------------------------------------
            # PC sperren
            # -------------------------------------------------

            "sperre meinen pc",
            "sperr meinen pc",
            "sperre den pc",
            "sperr den pc",
            "sperre meinen computer",
            "sperr meinen computer",
            "sperre den computer",
            "sperr den computer",
            "pc sperren",
            "computer sperren",

            # -------------------------------------------------
            # Herunterfahren
            # -------------------------------------------------

            "fahre meinen pc herunter",
            "fahr meinen pc herunter",
            "fahre den pc herunter",
            "fahr den pc herunter",
            "fahre meinen computer herunter",
            "fahr meinen computer herunter",
            "pc herunterfahren",
            "computer herunterfahren",
            "herunterfahren",

            # -------------------------------------------------
            # Neustart
            # -------------------------------------------------

            "starte meinen pc neu",
            "starte den pc neu",
            "starte meinen computer neu",
            "starte den computer neu",
            "pc neu starten",
            "computer neu starten",
            "pc neustarten",
            "computer neustarten",

            # -------------------------------------------------
            # Windows-Einstellungen
            # -------------------------------------------------

            "öffne die einstellungen",
            "öffne einstellungen",
            "öffne die windows einstellungen",
            "öffne windows einstellungen",

            # -------------------------------------------------
            # Taschenrechner
            # -------------------------------------------------

            "öffne den taschenrechner",
            "öffne taschenrechner",
            "öffne den rechner",
            "öffne rechner",

            # -------------------------------------------------
            # Notepad / Editor
            # -------------------------------------------------

            "öffne notepad",
            "öffne den editor",
            "öffne editor",

            # -------------------------------------------------
            # Desktop anzeigen
            # -------------------------------------------------

            "zeige den desktop",
            "zeig den desktop",
            "zeige mir den desktop",
            "zeig mir den desktop",
            "desktop anzeigen",
            "desktop zeigen",

            # -------------------------------------------------
            # Fenster minimieren
            # -------------------------------------------------

            "minimiere das fenster",
            "minimiere den fenster",
            "fenster minimieren",
            "minimieren",

            # -------------------------------------------------
            # Fenster maximieren
            # -------------------------------------------------

            "maximiere das fenster",
            "maximiere den fenster",
            "fenster maximieren",
            "maximieren",

            # -------------------------------------------------
            # Fenster schließen
            # -------------------------------------------------

            "schließe das fenster",
            "schliess das fenster",
            "fenster schließen",
            "fenster schliessen",

            # -------------------------------------------------
            # Fenster wechseln
            # -------------------------------------------------

            "wechsle das fenster",
            "wechsel das fenster",
            "fenster wechseln",
            "wechsle fenster",
            "wechsel fenster",
            "nächstes fenster",
            "naechstes fenster",
        )

        return any(command in prompt for command in commands)

    def confidence(self, prompt: str) -> float:
        if self.can_handle(prompt):
            return 1.0

        return 0.0

    def execute(self, prompt: str) -> str:
        prompt = prompt.lower().strip()

        # -----------------------------------------------------
        # PC sperren
        # -----------------------------------------------------

        if (
            "sperre meinen pc" in prompt
            or "sperr meinen pc" in prompt
            or "sperre den pc" in prompt
            or "sperr den pc" in prompt
            or "sperre meinen computer" in prompt
            or "sperr meinen computer" in prompt
            or "sperre den computer" in prompt
            or "sperr den computer" in prompt
            or prompt == "pc sperren"
            or prompt == "computer sperren"
        ):
            return (
                "Die PC-Sperre ist erkannt. "
                "Die eigentliche Aktion wird später über eine "
                "Sicherheitsbestätigung ausgeführt."
            )

        # -----------------------------------------------------
        # Herunterfahren
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # Neustart
        # -----------------------------------------------------

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

        # -----------------------------------------------------
        # Windows-Einstellungen
        # -----------------------------------------------------

        if (
            "öffne die einstellungen" in prompt
            or "öffne einstellungen" in prompt
            or "öffne die windows einstellungen" in prompt
            or "öffne windows einstellungen" in prompt
        ):
            if SystemActions.open_settings():
                return "Die Windows-Einstellungen wurden geöffnet."

            return "Die Windows-Einstellungen konnten nicht geöffnet werden."

        # -----------------------------------------------------
        # Taschenrechner
        # -----------------------------------------------------

        if (
            "taschenrechner" in prompt
            or prompt == "öffne den rechner"
            or prompt == "öffne rechner"
        ):
            if SystemActions.open_calculator():
                return "Der Taschenrechner wurde geöffnet."

            return "Der Taschenrechner konnte nicht gestartet werden."

        # -----------------------------------------------------
        # Notepad / Editor
        # -----------------------------------------------------

        if (
            "notepad" in prompt
            or "editor" in prompt
        ):
            if SystemActions.open_notepad():
                return "Notepad wurde geöffnet."

            return "Notepad konnte nicht gestartet werden."

        # -----------------------------------------------------
        # Desktop anzeigen
        # -----------------------------------------------------

        if (
            "zeige den desktop" in prompt
            or "zeig den desktop" in prompt
            or "zeige mir den desktop" in prompt
            or "zeig mir den desktop" in prompt
            or "desktop anzeigen" in prompt
            or "desktop zeigen" in prompt
        ):
            if SystemActions.show_desktop():
                return "Der Desktop wird angezeigt."

            return "Der Desktop konnte nicht angezeigt werden."

        # -----------------------------------------------------
        # Fenster minimieren
        # -----------------------------------------------------

        if (
            "minimiere das fenster" in prompt
            or "minimiere den fenster" in prompt
            or "fenster minimieren" in prompt
            or prompt == "minimieren"
        ):
            if SystemActions.minimize_window():
                return "Das Fenster wurde minimiert."

            return "Das Fenster konnte nicht minimiert werden."

        # -----------------------------------------------------
        # Fenster maximieren
        # -----------------------------------------------------

        if (
            "maximiere das fenster" in prompt
            or "maximiere den fenster" in prompt
            or "fenster maximieren" in prompt
            or prompt == "maximieren"
        ):
            if SystemActions.maximize_window():
                return "Das Fenster wurde maximiert."

            return "Das Fenster konnte nicht maximiert werden."

        # -----------------------------------------------------
        # Fenster schließen
        # -----------------------------------------------------

        if (
            "schließe das fenster" in prompt
            or "schliess das fenster" in prompt
            or "fenster schließen" in prompt
            or "fenster schliessen" in prompt
        ):
            if SystemActions.close_window():
                return "Das Fenster wurde geschlossen."

            return "Das Fenster konnte nicht geschlossen werden."

        # -----------------------------------------------------
        # Fenster wechseln
        # -----------------------------------------------------

        if (
            "wechsle das fenster" in prompt
            or "wechsel das fenster" in prompt
            or "fenster wechseln" in prompt
            or "wechsle fenster" in prompt
            or "wechsel fenster" in prompt
            or "nächstes fenster" in prompt
            or "naechstes fenster" in prompt
        ):
            if SystemActions.switch_window():
                return "Ich habe zum nächsten Fenster gewechselt."

            return "Das Fenster konnte nicht gewechselt werden."

        return "Ich konnte diese Systemaktion nicht finden."