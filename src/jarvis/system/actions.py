from __future__ import annotations

import os
import subprocess


class SystemActions:
    """Führt sichere Systemaktionen unter Windows aus."""

    @staticmethod
    def open_notepad() -> bool:
        try:
            subprocess.Popen(["notepad.exe"])
            return True
        except OSError:
            return False

    @staticmethod
    def open_calculator() -> bool:
        try:
            subprocess.Popen(["calc.exe"])
            return True
        except OSError:
            return False

    @staticmethod
    def open_application(path: str) -> bool:
        """Startet eine Anwendung oder Windows-Verknüpfung."""

        if not path:
            return False

        try:
            path = os.path.expandvars(path)

            # Windows-Verknüpfungen (.lnk) direkt über Windows öffnen.
            if path.lower().endswith(".lnk"):
                os.startfile(path)
                return True

            # Normale ausführbare Dateien starten.
            subprocess.Popen([path])
            return True

        except (OSError, FileNotFoundError):
            return False