from __future__ import annotations

import os
import platform
import shutil
import sys

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
            "system info",
            "wie heißt mein computer",
            "wie heisst mein computer",
            "computername",
            "welche python version",
            "python version",
            "welche cpu",
            "welcher prozessor",
            "wie viel ram",
            "arbeitsspeicher",
            "freier speicher",
            "festplattenspeicher",
        )

        return any(keyword in prompt for keyword in keywords)

    def execute(self, prompt: str) -> str:
        prompt = prompt.lower()

        if "computer" in prompt or "computername" in prompt:
            return f"Der Computer heißt {platform.node()}."

        if "python" in prompt:
            return f"Du verwendest Python {platform.python_version()}."

        if "cpu" in prompt or "prozessor" in prompt:
            cpu = platform.processor()

            if not cpu:
                cpu = "unbekannt"

            return f"Dein Prozessor ist {cpu}."

        if "ram" in prompt or "arbeitsspeicher" in prompt:
            try:
                import ctypes

                class MemoryStatus(ctypes.Structure):
                    _fields_ = [
                        ("length", ctypes.c_ulong),
                        ("memory_load", ctypes.c_ulong),
                        ("total_phys", ctypes.c_ulonglong),
                        ("avail_phys", ctypes.c_ulonglong),
                        ("total_page_file", ctypes.c_ulonglong),
                        ("avail_page_file", ctypes.c_ulonglong),
                        ("total_virtual", ctypes.c_ulonglong),
                        ("avail_virtual", ctypes.c_ulonglong),
                        ("avail_extended_virtual", ctypes.c_ulonglong),
                    ]

                memory = MemoryStatus()
                memory.length = ctypes.sizeof(MemoryStatus)

                ctypes.windll.kernel32.GlobalMemoryStatusEx(
                    ctypes.byref(memory)
                )

                total_gb = memory.total_phys / (1024**3)

                return f"Dein Computer hat {total_gb:.1f} GB RAM."

            except (AttributeError, OSError):
                return "Die RAM-Information konnte nicht ermittelt werden."

        if "speicher" in prompt or "festplatte" in prompt:
            try:
                total, used, free = shutil.disk_usage(os.getcwd())

                free_gb = free / (1024**3)

                return f"Es sind noch {free_gb:.1f} GB Speicherplatz frei."

            except OSError:
                return "Der verfügbare Speicherplatz konnte nicht ermittelt werden."

        return (
            f"Du verwendest {platform.system()} "
            f"{platform.release()}."
        )