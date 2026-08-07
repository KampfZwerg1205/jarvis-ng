from __future__ import annotations

import platform

from jarvis.skills.base import Skill


class SystemSkill(Skill):
    """Stellt grundlegende Systeminformationen bereit."""

    @property
    def name(self) -> str:
        return "system"

    def can_handle(self, prompt: str) -> bool:
        prompt = prompt.lower()

        keywords = (
            "welches betriebssystem",
            "welches system",
            "systeminformationen",
            "wie heißt mein computer",
            "wie heisst mein computer",
            "computername",
        )

        return any(keyword in prompt for keyword in keywords)

    def execute(self, prompt: str) -> str:
        prompt = prompt.lower()

        if "computer" in prompt or "computername" in prompt:
            return f"Der Computer heißt {platform.node()}."

        return (
            f"Du verwendest {platform.system()} "
            f"{platform.release()}."
        )