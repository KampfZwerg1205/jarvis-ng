from __future__ import annotations

import platform
import socket
import getpass

from jarvis.skills.base import Skill


class SystemInfoSkill(Skill):
    """Liefert Informationen über das System."""

    @property
    def name(self) -> str:
        return "system_info"

    def can_handle(self, prompt: str) -> bool:
        prompt = prompt.lower()

        keywords = (
            "betriebssystem",
            "welches system",
            "mein pc",
            "computername",
            "pc name",
            "hostname",
        )

        return any(keyword in prompt for keyword in keywords)

    def confidence(self, prompt: str) -> float:
        if self.can_handle(prompt):
            return 1.0

        return 0.0

    def execute(self, prompt: str) -> str:
        prompt = prompt.lower()

        if "betriebssystem" in prompt or "system" in prompt:
            return (
                f"Du nutzt {platform.system()} "
                f"{platform.release()}."
            )

        if (
            "pc" in prompt
            or "computername" in prompt
            or "hostname" in prompt
        ):
            return (
                f"Der Name deines PCs ist "
                f"{socket.gethostname()}."
            )

        if "benutzer" in prompt:
            return (
                f"Du bist angemeldet als "
                f"{getpass.getuser()}."
            )

        return "Keine Systeminformation gefunden."