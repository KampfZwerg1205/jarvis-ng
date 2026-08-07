from __future__ import annotations

import os
import platform

from jarvis.skills.base import Skill


class SystemInfoSkill(Skill):
    """Liefert Informationen über das aktuelle System."""

    @property
    def name(self) -> str:
        return "system_info"

    def can_handle(self, prompt: str) -> bool:
        prompt = prompt.lower().strip()

        keywords = (
            "welches betriebssystem",
            "welches system",
            "was für ein betriebssystem",
            "was für ein system",
            "wie heißt mein pc",
            "wie heisst mein pc",
            "pc name",
            "computername",
            "hostname",
            "welchen prozessor",
            "welche cpu",
            "meine cpu",
            "wie viel ram",
            "wie viel arbeitsspeicher",
            "arbeitsspeicher",
        )

        return any(keyword in prompt for keyword in keywords)

    def confidence(self, prompt: str) -> float:
        if self.can_handle(prompt):
            return 1.0

        return 0.0

    def execute(self, prompt: str) -> str:
        prompt = prompt.lower().strip()

        # Betriebssystem
        if (
            "betriebssystem" in prompt
            or "welches system" in prompt
            or "was für ein system" in prompt
        ):
            system = platform.system()
            release = platform.release()

            return f"Du verwendest {system} {release}."

        # PC-Name
        if (
            "wie heißt mein pc" in prompt
            or "wie heisst mein pc" in prompt
            or "pc name" in prompt
            or "computername" in prompt
            or "hostname" in prompt
        ):
            hostname = platform.node()

            return f"Der Name deines PCs ist {hostname}."

        # Prozessor
        if (
            "prozessor" in prompt
            or "welche cpu" in prompt
            or "meine cpu" in prompt
        ):
            processor = platform.processor()

            if not processor:
                processor = "unbekannt"

            return f"Dein Prozessor ist {processor}."

        # RAM
        if (
            "wie viel ram" in prompt
            or "arbeitsspeicher" in prompt
        ):
            try:
                import psutil

                ram_gb = psutil.virtual_memory().total / (1024 ** 3)

                return f"Du hast {ram_gb:.1f} GB Arbeitsspeicher."

            except ImportError:
                return "Die RAM-Information ist momentan nicht verfügbar."

        return "Diese Systeminformation wird noch nicht unterstützt."