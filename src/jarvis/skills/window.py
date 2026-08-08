from __future__ import annotations

from jarvis.skills.base import Skill
from jarvis.system.actions import SystemActions


class WindowSkill(Skill):
    """Steuert aktive Windows-Fenster."""

    @property
    def name(self) -> str:
        return "window"

    def can_handle(self, prompt: str) -> bool:
        prompt = prompt.lower().strip()

        commands = (
            "fenster minimieren",
            "fenster maximiere",
            "fenster maximieren",
            "fenster schließen",
            "fenster schließe",
            "desktop anzeigen",
            "zeige den desktop",
            "zeige desktop",
            "wechsel das fenster",
            "wechsle das fenster",
            "wechsel zum nächsten fenster",
            "wechsle zum nächsten fenster",
        )

        return any(command in prompt for command in commands)

    def confidence(self, prompt: str) -> float:
        if self.can_handle(prompt):
            return 1.0

        return 0.0

    def execute(self, prompt: str) -> str:
        prompt = prompt.lower().strip()

        # Fenster minimieren
        if "fenster minimieren" in prompt:
            if SystemActions.minimize_window():
                return "Das Fenster wurde minimiert."

            return "Das Fenster konnte nicht minimiert werden."

        # Fenster maximieren
        if (
            "fenster maximieren" in prompt
            or "fenster maximiere" in prompt
        ):
            if SystemActions.maximize_window():
                return "Das Fenster wurde maximiert."

            return "Das Fenster konnte nicht maximiert werden."

        # Fenster schließen
        if (
            "fenster schließen" in prompt
            or "fenster schließe" in prompt
        ):
            if SystemActions.close_window():
                return "Das Fenster wurde geschlossen."

            return "Das Fenster konnte nicht geschlossen werden."

        # Desktop anzeigen
        if (
            "desktop anzeigen" in prompt
            or "zeige den desktop" in prompt
            or "zeige desktop" in prompt
        ):
            if SystemActions.show_desktop():
                return "Der Desktop wird angezeigt."

            return "Der Desktop konnte nicht angezeigt werden."

        # Fenster wechseln
        if (
            "wechsel das fenster" in prompt
            or "wechsle das fenster" in prompt
            or "wechsel zum nächsten fenster" in prompt
            or "wechsle zum nächsten fenster" in prompt
        ):
            if SystemActions.switch_window():
                return "Zum nächsten Fenster gewechselt."

            return "Das Fenster konnte nicht gewechselt werden."

        return "Dieser Fensterbefehl wird noch nicht unterstützt."