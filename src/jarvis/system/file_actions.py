from __future__ import annotations

import os
import subprocess
from pathlib import Path


class FileActions:
    """Führt sichere Datei- und Ordneraktionen unter Windows aus."""

    @staticmethod
    def open_path(path: str | Path) -> bool:
        """Öffnet einen Ordner oder eine Datei mit der Standardanwendung."""

        try:
            target = Path(path).expanduser()

            if not target.exists():
                return False

            os.startfile(str(target))
            return True

        except OSError:
            return False

    @staticmethod
    def open_downloads() -> bool:
        """Öffnet den Downloads-Ordner."""

        downloads = Path.home() / "Downloads"
        return FileActions.open_path(downloads)

    @staticmethod
    def open_documents() -> bool:
        """Öffnet den Dokumente-Ordner."""

        documents = Path.home() / "Documents"
        return FileActions.open_path(documents)

    @staticmethod
    def open_desktop() -> bool:
        """Öffnet den Desktop-Ordner."""

        desktop = Path.home() / "Desktop"
        return FileActions.open_path(desktop)

    @staticmethod
    def open_pictures() -> bool:
        """Öffnet den Bilder-Ordner."""

        pictures = Path.home() / "Pictures"
        return FileActions.open_path(pictures)

    @staticmethod
    def open_videos() -> bool:
        """Öffnet den Videos-Ordner."""

        videos = Path.home() / "Videos"
        return FileActions.open_path(videos)

    @staticmethod
    def open_music() -> bool:
        """Öffnet den Musik-Ordner."""

        music = Path.home() / "Music"
        return FileActions.open_path(music)

    @staticmethod
    def open_recycle_bin() -> bool:
        """Öffnet den Windows-Papierkorb."""

        try:
            subprocess.Popen(
                [
                    "explorer.exe",
                    "shell:RecycleBinFolder",
                ]
            )

            return True

        except OSError:
            return False