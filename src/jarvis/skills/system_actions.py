from __future__ import annotations

from jarvis.skills.base import Skill
from jarvis.system.actions import SystemActions


class SystemActionSkill(Skill):
    """Führt sichere, vordefinierte Systemaktionen aus."""

    @property
    def name(self) -> str:
        return "system_actions"

    def can_handle(self, prompt: str) -> bool:
        prompt = prompt.lower()

        commands = (
            "öffne notepad",
            "öffne editor",
            "öffne taschenrechner",
            "öffne den taschenrechner",
            "öffne rechner",
            "öffne den rechner",
        )

        return any(command in prompt for command in commands)

    def execute(self, prompt: str) -> str:
        prompt = prompt.lower()

        if "notepad" in prompt or "editor" in prompt:
            SystemActions.open_notepad()
            return "Notepad wurde geöffnet."

        if "taschenrechner" in prompt or "rechner" in prompt:
            SystemActions.open_calculator()
            return "Der Taschenrechner wurde geöffnet."

        return "Diese Systemaktion wird nicht unterstützt."