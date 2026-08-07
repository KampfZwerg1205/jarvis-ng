from __future__ import annotations

from datetime import datetime

from jarvis.skills.base import Skill


class TimeSkill(Skill):
    """Stellt die aktuelle Uhrzeit bereit."""

    @property
    def name(self) -> str:
        return "time"

    def can_handle(self, prompt: str) -> bool:
        prompt = prompt.lower()

        keywords = (
            "wie spät",
            "uhrzeit",
            "wie viel uhr",
            "welche uhrzeit",
        )

        return any(keyword in prompt for keyword in keywords)

    def confidence(self, prompt: str) -> float:
        if self.can_handle(prompt):
            return 0.9

        return 0.0

    def execute(self, prompt: str) -> str:
        current_time = datetime.now().strftime("%H:%M:%S")

        return f"Es ist {current_time} Uhr."