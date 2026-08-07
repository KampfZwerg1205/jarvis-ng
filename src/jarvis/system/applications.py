from __future__ import annotations

from pathlib import Path


class ApplicationScanner:
    """Findet installierte Windows-Anwendungen."""

    def __init__(self) -> None:
        self.locations = [
            Path(
                r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs"
            ),
            Path.home()
            / "AppData"
            / "Roaming"
            / "Microsoft"
            / "Windows"
            / "Start Menu"
            / "Programs",
        ]

    def scan(self) -> dict[str, str]:
        apps: dict[str, str] = {}

        for location in self.locations:
            if not location.exists():
                continue

            for shortcut in location.rglob("*.lnk"):
                name = shortcut.stem.lower()

                apps[name] = str(shortcut)

        return apps