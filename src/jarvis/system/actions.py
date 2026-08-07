from __future__ import annotations

import os
import subprocess


class SystemActions:
    """Führt Systemaktionen aus."""

    @staticmethod
    def open_notepad() -> bool:
        try:
            subprocess.Popen(
                ["notepad.exe"],
                shell=True,
            )

            return True

        except Exception:
            return False


    @staticmethod
    def open_calculator() -> bool:
        try:
            subprocess.Popen(
                ["calc.exe"],
                shell=True,
            )

            return True

        except Exception:
            return False


    @staticmethod
    def open_application(path: str) -> bool:
        """
        Öffnet eine gefundene Anwendung.
        Unterstützt .exe und .lnk Dateien.
        """

        try:
            os.startfile(path)

            return True

        except Exception:
            return False