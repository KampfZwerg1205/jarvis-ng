from __future__ import annotations

from jarvis.skills.base import Skill
from jarvis.system.actions import SystemActions


class MediaSkill(Skill):
    """Steuert die Medienwiedergabe unter Windows."""

    @property
    def name(self) -> str:
        return "media"

    def can_handle(self, prompt: str) -> bool:
        prompt = prompt.lower().strip()

        commands = (
            "pause",
            "pausiere",
            "weiter",
            "fortsetzen",
            "wiedergabe",
            "nächster titel",
            "naechster titel",
            "nächster song",
            "naechster song",
            "nächstes lied",
            "naechstes lied",
            "vorheriger titel",
            "vorheriger song",
            "vorheriges lied",
        )

        return any(command in prompt for command in commands)

    def confidence(self, prompt: str) -> float:
        if self.can_handle(prompt):
            return 1.0

        return 0.0

    def execute(self, prompt: str) -> str:
        prompt = prompt.lower().strip()

        # Nächster Titel
        if (
            "nächster titel" in prompt
            or "naechster titel" in prompt
            or "nächster song" in prompt
            or "naechster song" in prompt
            or "nächstes lied" in prompt
            or "naechstes lied" in prompt
        ):
            if SystemActions.media_next():
                return "Der nächste Titel wurde ausgewählt."

            return "Der nächste Titel konnte nicht ausgewählt werden."

        # Vorheriger Titel
        if (
            "vorheriger titel" in prompt
            or "vorheriger song" in prompt
            or "vorheriges lied" in prompt
        ):
            if SystemActions.media_previous():
                return "Der vorherige Titel wurde ausgewählt."

            return "Der vorherige Titel konnte nicht ausgewählt werden."

        # Pause
        if (
            "pause" in prompt
            or "pausiere" in prompt
        ):
            if SystemActions.media_play_pause():
                return "Die Wiedergabe wurde pausiert."

            return "Die Wiedergabe konnte nicht pausiert werden."

        # Weiter / Fortsetzen
        if (
            "weiter" in prompt
            or "fortsetzen" in prompt
            or "wiedergabe" in prompt
        ):
            if SystemActions.media_play_pause():
                return "Die Wiedergabe wurde fortgesetzt."

            return "Die Wiedergabe konnte nicht fortgesetzt werden."

        return "Dieser Medienbefehl wird noch nicht unterstützt."