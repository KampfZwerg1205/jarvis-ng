from __future__ import annotations

import os
import subprocess

from jarvis.skills.base import Skill
from jarvis.system.applications import ApplicationScanner


class AppLauncherSkill(Skill):
    """Startet installierte Programme."""

    def __init__(self) -> None:
        self.scanner = ApplicationScanner()

    @property
    def name(self) -> str:
        return "app_launcher"

    def can_handle(self, prompt: str) -> bool:
        prompt = prompt.lower()

        commands = (
            "öffne",
            "starte",
            "launch",
        )

        return any(command in prompt for command in commands)

    def confidence(self, prompt: str) -> float:
        if self.can_handle(prompt):
            return 0.8

        return 0.0

    def execute(self, prompt: str) -> str:
        prompt = prompt.lower()

        applications = self.scanner.scan()

        for app_name, shortcut in applications.items():
            if app_name in prompt:
                os.startfile(shortcut)

                return f"{app_name} wurde gestartet."

        return "Diese Anwendung wurde nicht gefunden."