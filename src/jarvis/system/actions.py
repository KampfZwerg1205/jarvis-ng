from __future__ import annotations

import subprocess


class SystemActions:
    """Sichere, vordefinierte Systemaktionen."""

    @staticmethod
    def open_notepad() -> None:
        subprocess.Popen(["notepad.exe"])

    @staticmethod
    def open_calculator() -> None:
        subprocess.Popen(["calc.exe"])