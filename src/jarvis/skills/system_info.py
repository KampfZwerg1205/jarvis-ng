from __future__ import annotations

import platform
import shutil

from jarvis.skills.base import Skill


class SystemInfoSkill(Skill):
    """Liefert Informationen über das aktuelle System."""

    @property
    def name(self) -> str:
        return "system_info"

    def can_handle(self, prompt: str) -> bool:
        prompt = prompt.lower().strip()

        keywords = (
            # Betriebssystem
            "welches betriebssystem",
            "was für ein betriebssystem",
            "welches system",
            "was für ein system",
            "welche windows version",
            "windows version",

            # PC-Name
            "wie heißt mein pc",
            "wie heisst mein pc",
            "pc name",
            "computername",
            "hostname",
            "wie heißt der pc",
            "wie heisst der pc",

            # Prozessor
            "welchen prozessor",
            "welche cpu",
            "meine cpu",
            "was für einen prozessor",

            # RAM
            "wie viel ram",
            "wie viel arbeitsspeicher",
            "arbeitsspeicher",
            "ram",

            # Grafikkarte
            "welche grafikkarte",
            "meine grafikkarte",
            "welche gpu",
            "meine gpu",
            "was für eine grafikkarte",

            # Speicher
            "wie viel speicher",
            "wie viel festplatte",
            "freier speicher",
            "festplattenspeicher",
        )

        return any(keyword in prompt for keyword in keywords)

    def confidence(self, prompt: str) -> float:
        if self.can_handle(prompt):
            return 1.0

        return 0.0

    def execute(self, prompt: str) -> str:
        prompt = prompt.lower().strip()

        # ---------------------------------------------------------
        # Betriebssystem
        # ---------------------------------------------------------

        if (
            "betriebssystem" in prompt
            or "welches system" in prompt
            or "was für ein system" in prompt
            or "welche windows version" in prompt
            or "windows version" in prompt
        ):
            system = platform.system()
            release = platform.release()

            if system == "Windows":
                return f"Du verwendest Windows {release}."

            return f"Du verwendest {system} {release}."

        # ---------------------------------------------------------
        # PC-Name
        # ---------------------------------------------------------

        if (
            "wie heißt mein pc" in prompt
            or "wie heisst mein pc" in prompt
            or "wie heißt der pc" in prompt
            or "wie heisst der pc" in prompt
            or "pc name" in prompt
            or "computername" in prompt
            or "hostname" in prompt
        ):
            hostname = platform.node()

            if not hostname:
                return "Der Name deines PCs konnte nicht ermittelt werden."

            return f"Der Name deines PCs ist {hostname}."

        # ---------------------------------------------------------
        # Prozessor
        # ---------------------------------------------------------

        if (
            "prozessor" in prompt
            or "welche cpu" in prompt
            or "meine cpu" in prompt
        ):
            processor = platform.processor()

            if not processor:
                processor = "unbekannt"

            return f"Dein Prozessor ist {processor}."

        # ---------------------------------------------------------
        # RAM
        # ---------------------------------------------------------

        if (
            "wie viel ram" in prompt
            or "arbeitsspeicher" in prompt
            or prompt == "ram"
        ):
            try:
                import psutil

                ram_gb = psutil.virtual_memory().total / (1024 ** 3)

                return f"Du hast {ram_gb:.1f} GB Arbeitsspeicher."

            except ImportError:
                return (
                    "Die RAM-Information ist momentan nicht verfügbar. "
                    "Bitte installiere psutil."
                )

        # ---------------------------------------------------------
        # Grafikkarte
        # ---------------------------------------------------------

        if (
            "grafikkarte" in prompt
            or "welche gpu" in prompt
            or "meine gpu" in prompt
        ):
            try:
                import subprocess

                result = subprocess.run(
                    [
                        "powershell",
                        "-NoProfile",
                        "-Command",
                        "Get-CimInstance Win32_VideoController "
                        "| Select-Object -ExpandProperty Name"
                    ],
                    capture_output=True,
                    text=True,
                    check=False,
                )

                gpu_names = [
                    line.strip()
                    for line in result.stdout.splitlines()
                    if line.strip()
                ]

                if gpu_names:
                    return f"Deine Grafikkarte ist {gpu_names[0]}."

                return "Die Grafikkarte konnte nicht ermittelt werden."

            except Exception:
                return "Die Grafikkarten-Information ist momentan nicht verfügbar."

        # ---------------------------------------------------------
        # Speicherplatz
        # ---------------------------------------------------------

        if (
            "wie viel speicher" in prompt
            or "wie viel festplatte" in prompt
            or "freier speicher" in prompt
            or "festplattenspeicher" in prompt
        ):
            try:
                total, used, free = shutil.disk_usage("C:\\")

                total_gb = total / (1024 ** 3)
                free_gb = free / (1024 ** 3)

                return (
                    f"Auf Laufwerk C: hast du "
                    f"{free_gb:.1f} GB freien Speicher "
                    f"von insgesamt {total_gb:.1f} GB."
                )

            except OSError:
                return "Die Speicherplatz-Information konnte nicht ermittelt werden."

        return "Diese Systeminformation wird noch nicht unterstützt."