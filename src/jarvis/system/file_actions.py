from __future__ import annotations

import os
import shutil
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

    @staticmethod
    def copy_file(
        source: str | Path,
        destination: str | Path,
    ) -> bool:
        """Kopiert eine Datei an ein Ziel."""

        try:
            source_path = Path(source).expanduser()
            destination_path = Path(destination).expanduser()

            if not source_path.exists():
                return False

            if not source_path.is_file():
                return False

            destination_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            shutil.copy2(
                source_path,
                destination_path,
            )

            return True

        except OSError:
            return False

    @staticmethod
    def move_file(
        source: str | Path,
        destination: str | Path,
    ) -> bool:
        """Verschiebt eine Datei an ein Ziel."""

        try:
            source_path = Path(source).expanduser()
            destination_path = Path(destination).expanduser()

            if not source_path.exists():
                return False

            if not source_path.is_file():
                return False

            destination_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            shutil.move(
                str(source_path),
                str(destination_path),
            )

            return True

        except OSError:
            return False

    @staticmethod
    def rename_file(
        source: str | Path,
        new_name: str,
    ) -> bool:
        """Benennt eine Datei um."""

        try:
            source_path = Path(source).expanduser()

            if not source_path.exists():
                return False

            if not source_path.is_file():
                return False

            new_name = new_name.strip()

            if not new_name:
                return False

            # Der neue Name darf nur ein Dateiname sein.
            # Es darf kein zusätzlicher Pfad angegeben werden.
            if Path(new_name).name != new_name:
                return False

            destination = source_path.with_name(new_name)

            # Vorhandene Dateien werden nicht überschrieben.
            if destination.exists():
                return False

            source_path.rename(destination)

            return True

        except OSError:
            return False

    @staticmethod
    def delete_file(
        source: str | Path,
    ) -> bool:
        """Löscht eine einzelne Datei."""

        try:
            source_path = Path(source).expanduser()

            if not source_path.exists():
                return False

            # Sicherheitsregel:
            # Diese Methode löscht ausschließlich Dateien,
            # niemals komplette Ordner.
            if not source_path.is_file():
                return False

            source_path.unlink()

            return True

        except OSError:
            return False