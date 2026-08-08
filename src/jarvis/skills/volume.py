from __future__ import annotations

from jarvis.skills.base import Skill
from jarvis.system.actions import SystemActions


class VolumeSkill(Skill):
    """Steuert die Windows-Lautstärke."""

    @property
    def name(self) -> str:
        return "volume"

    def can_handle(self, prompt: str) -> bool:
        prompt = prompt.lower().strip()

        commands = (
            "mach lauter",
            "mach leiser",
            "lautstärke erhöhen",
            "lautstärke verringern",
            "lautstärke erhöhen",
            "lauter",
            "leiser",
            "stumm",
            "stumm schalten",
            "ton aus",
            "ton an",
        )

        return any(command in prompt for command in commands)

    def confidence(self, prompt: str) -> float:
        if self.can_handle(prompt):
            return 1.0

        return 0.0

    def execute(self, prompt: str) -> str:
        prompt = prompt.lower().strip()

        # Stummschalten
        if (
            "stumm" in prompt
            or "ton aus" in prompt
            or "ton an" in prompt
        ):
            if SystemActions.volume_mute():
                return "Der Ton wurde umgeschaltet."

            return "Der Ton konnte nicht umgeschaltet werden."

        # Lauter
        if (
            "mach lauter" in prompt
            or "lautstärke erhöhen" in prompt
            or "lauter" in prompt
        ):
            if SystemActions.volume_up():
                return "Die Lautstärke wurde erhöht."

            return "Die Lautstärke konnte nicht erhöht werden."

        # Leiser
        if (
            "mach leiser" in prompt
            or "lautstärke verringern" in prompt
            or "leiser" in prompt
        ):
            if SystemActions.volume_down():
                return "Die Lautstärke wurde verringert."

            return "Die Lautstärke konnte nicht verringert werden."

        return "Dieser Lautstärkebefehl wird noch nicht unterstützt."