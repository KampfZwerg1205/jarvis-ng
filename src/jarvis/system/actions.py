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

    # ---------------------------------------------------------
    # Lautstärke
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # Mediensteuerung
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # Fenstersteuerung
    # ---------------------------------------------------------

    @staticmethod
    def minimize_window() -> bool:
        """Minimiert das aktuell aktive Fenster."""

        try:
            import ctypes

            user32 = ctypes.windll.user32

            hwnd = user32.GetForegroundWindow()

            if not hwnd:
                return False

            user32.ShowWindow(hwnd, 6)

            return True

        except OSError:
            return False

    @staticmethod
    def maximize_window() -> bool:
        """Maximiert das aktuell aktive Fenster."""

        try:
            import ctypes

            user32 = ctypes.windll.user32

            hwnd = user32.GetForegroundWindow()

            if not hwnd:
                return False

            user32.ShowWindow(hwnd, 3)

            return True

        except OSError:
            return False

    @staticmethod
    def close_window() -> bool:
        """Schließt das aktuell aktive Fenster."""

        try:
            import ctypes

            user32 = ctypes.windll.user32

            hwnd = user32.GetForegroundWindow()

            if not hwnd:
                return False

            WM_CLOSE = 0x0010

            user32.PostMessageW(
                hwnd,
                WM_CLOSE,
                0,
                0,
            )

            return True

        except OSError:
            return False

    @staticmethod
    def show_desktop() -> bool:
        """Zeigt den Windows-Desktop an."""

        try:
            subprocess.Popen(
                [
                    "explorer.exe",
                    "shell:::{3080F90D-D7AD-11D9-BD98-0000947B0257}",
                ]
            )

            return True

        except OSError:
            return False

    @staticmethod
    def switch_window() -> bool:
        """Wechselt zum nächsten Windows-Fenster."""

        try:
            import ctypes

            user32 = ctypes.windll.user32

            VK_MENU = 0x12
            VK_TAB = 0x09
            KEYEVENTF_KEYUP = 0x0002

            user32.keybd_event(VK_MENU, 0, 0, 0)
            user32.keybd_event(VK_TAB, 0, 0, 0)
            user32.keybd_event(
                VK_TAB,
                0,
                KEYEVENTF_KEYUP,
                0,
            )
            user32.keybd_event(
                VK_MENU,
                0,
                KEYEVENTF_KEYUP,
                0,
            )

            return True

        except OSError:
            return False