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

            if path.lower().endswith(".lnk"):
                os.startfile(path)
                return True

            subprocess.Popen([path])
            return True

        except (OSError, FileNotFoundError):
            return False

    @staticmethod
    def lock_pc() -> bool:
        """Sperrt den Windows-PC."""

        try:
            result = subprocess.run(
                ["rundll32.exe", "user32.dll,LockWorkStation"],
                check=False,
            )

            return result.returncode == 0

        except OSError:
            return False

    @staticmethod
    def restart_pc() -> bool:
        """Startet Windows neu."""

        try:
            subprocess.Popen(
                ["shutdown.exe", "/r", "/t", "0"]
            )
            return True

        except OSError:
            return False

    @staticmethod
    def shutdown_pc() -> bool:
        """Fährt Windows herunter."""

        try:
            subprocess.Popen(
                ["shutdown.exe", "/s", "/t", "0"]
            )
            return True

        except OSError:
            return False

    @staticmethod
    def open_settings() -> bool:
        """Öffnet die Windows-Einstellungen."""

        try:
            os.startfile("ms-settings:")
            return True

        except OSError:
            return False

    @staticmethod
    def volume_up() -> bool:
        """Erhöht die Windows-Lautstärke."""

        try:
            import ctypes

            user32 = ctypes.windll.user32

            for _ in range(5):
                user32.keybd_event(0xAF, 0, 0, 0)
                user32.keybd_event(0xAF, 0, 2, 0)

            return True

        except OSError:
            return False

    @staticmethod
    def volume_down() -> bool:
        """Verringert die Windows-Lautstärke."""

        try:
            import ctypes

            user32 = ctypes.windll.user32

            for _ in range(5):
                user32.keybd_event(0xAE, 0, 0, 0)
                user32.keybd_event(0xAE, 0, 2, 0)

            return True

        except OSError:
            return False

    @staticmethod
    def volume_mute() -> bool:
        """Schaltet den Windows-Ton stumm bzw. wieder ein."""

        try:
            import ctypes

            user32 = ctypes.windll.user32

            user32.keybd_event(0xAD, 0, 0, 0)
            user32.keybd_event(0xAD, 0, 2, 0)

            return True

        except OSError:
            return False

    @staticmethod
    def media_play_pause() -> bool:
        """Startet oder pausiert die Medienwiedergabe."""

        try:
            import ctypes

            user32 = ctypes.windll.user32

            user32.keybd_event(0xB3, 0, 0, 0)
            user32.keybd_event(0xB3, 0, 2, 0)

            return True

        except OSError:
            return False

    @staticmethod
    def media_next() -> bool:
        """Springt zum nächsten Titel."""

        try:
            import ctypes

            user32 = ctypes.windll.user32

            user32.keybd_event(0xB0, 0, 0, 0)
            user32.keybd_event(0xB0, 0, 2, 0)

            return True

        except OSError:
            return False

    @staticmethod
    def media_previous() -> bool:
        """Springt zum vorherigen Titel."""

        try:
            import ctypes

            user32 = ctypes.windll.user32

            user32.keybd_event(0xB1, 0, 0, 0)
            user32.keybd_event(0xB1, 0, 2, 0)

            return True

        except OSError:
            return False