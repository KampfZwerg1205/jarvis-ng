from __future__ import annotations

from pathlib import Path

from jarvis.skills.base import Skill
from jarvis.system.file_actions import FileActions


class FileDeleteSkill(Skill):
    """Löscht bekannte Dateien unter Windows."""

    @property
    def name(self) -> str:
        return "file_delete"

    def can_handle(self, prompt: str) -> bool:
        prompt = prompt.lower().strip()

        commands = (
            "lösche ",
            "lösch ",
            "entferne ",
            "entfern ",
            "delete ",
        )

        return any(
            prompt.startswith(command)
            for command in commands
        )

    def confidence(self, prompt: str) -> float:
        if self.can_handle(prompt):
            return 1.0

        return 0.0

    def execute(self, prompt: str) -> str:
        filename = self._parse_command(prompt)

        if filename is None:
            return "Ich konnte die zu löschende Datei nicht erkennen."

        source = self._find_source(filename)

        if source is None:
            return f"Ich konnte '{filename}' nicht finden."

        if FileActions.delete_file(source):
            return f"Ich habe '{source.name}' gelöscht."

        return f"'{source.name}' konnte nicht gelöscht werden."

    def _parse_command(self, prompt: str) -> str | None:
        """Extrahiert den Dateinamen aus dem Löschbefehl."""

        text = prompt.lower().strip()

        commands = (
            "lösche ",
            "lösch ",
            "entferne ",
            "entfern ",
            "delete ",
        )

        for command in commands:
            if text.startswith(command):
                text = text[len(command):]
                break
        else:
            return None

        text = text.strip(" .,!?")

        if text.endswith(" bitte"):
            text = text[:-6].strip()

        if not text:
            return None

        # Ein Pfad darf hier nicht angegeben werden.
        # JARVIS sucht ausschließlich in den bekannten Benutzerordnern.
        if Path(text).name != text:
            return None

        return text

    def _find_source(self, filename: str) -> Path | None:
        """Sucht die Datei in bekannten Benutzerordnern."""

        home = Path.home()

        folders = (
            home / "Downloads",
            home / "Documents",
            home / "Desktop",
            home / "Pictures",
            home / "Videos",
            home / "Music",
        )

        search_name = filename.lower().strip()

        for folder in folders:
            if not folder.exists():
                continue

            try:
                for path in folder.rglob("*"):
                    if path.is_file() and path.name.lower() == search_name:
                        return path

            except OSError:
                continue

        return None