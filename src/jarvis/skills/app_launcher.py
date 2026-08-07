from __future__ import annotations

import os
import subprocess

from jarvis.skills.base import Skill


class AppLauncherSkill(Skill):
    """Startet installierte Programme."""

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

        apps = {
            "firefox": [
                r"C:\Program Files\Mozilla Firefox\firefox.exe",
                r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
            ],

            "discord": [
                os.path.expandvars(
                    r"%LOCALAPPDATA%\Discord\Update.exe"
                ),
            ],

            "vscode": [
                os.path.expandvars(
                    r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe"
                ),
            ],

            "visual studio code": [
                os.path.expandvars(
                    r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe"
                ),
            ],

            "steam": [
                r"C:\Program Files (x86)\Steam\steam.exe",
            ],

            "spotify": [
                os.path.expandvars(
                    r"%APPDATA%\Spotify\Spotify.exe"
                ),
            ],
        }

        for name, paths in apps.items():
            if name in prompt:

                for path in paths:
                    if os.path.exists(path):
                        subprocess.Popen(path)
                        return f"{name} wurde gestartet."

                return (
                    f"{name} wurde gefunden, "
                    "aber der Installationspfad wurde nicht gefunden."
                )

        return "Diese Anwendung kenne ich noch nicht."