from __future__ import annotations

from jarvis.skills.base import Skill
from jarvis.system.file_actions import FileActions


class FileRecycleBinSkill(Skill):
    """Öffnet den Windows-Papierkorb."""

    @property
    def name(self) -> str:
        return "file_recycle_bin"

    def can_handle(self, prompt: str) -> bool:
        prompt = prompt.lower().strip()

        commands = (
        "öffne den papierkorb",
        "öffne papierkorb",
        "zeige den papierkorb",
        "zeige papierkorb",
        "zeige mir den papierkorb",
        "zeige mir papierkorb",
        "öffne den mülleimer",
        "öffne mülleimer",
        "zeige den mülleimer",
        "zeige mir den mülleimer",
        )

        return any(
            command in prompt
            for command in commands
        )

    def confidence(self, prompt: str) -> float:
        if self.can_handle(prompt):
            return 1.0

        return 0.0

    def execute(self, prompt: str) -> str:
        if FileActions.open_recycle_bin():
            return "Der Papierkorb wurde geöffnet."

        return "Der Papierkorb konnte nicht geöffnet werden."