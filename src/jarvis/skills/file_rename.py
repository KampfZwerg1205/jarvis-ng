from __future__ import annotations

from pathlib import Path

from jarvis.skills.base import Skill
from jarvis.system.file_actions import FileActions


class FileRenameSkill(Skill):
    """Benennt bekannte Dateien unter Windows um."""

    @property
    def name(self) -> str:
        return "file_rename"

    def can_handle(self, prompt: str) -> bool:
        prompt = prompt.lower().strip()

        commands = (
            "benenne ",
            "benenn ",
            "umbenennen ",
            "rename ",
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
        source_name, new_name = self._parse_command(prompt)

        if source_name is None:
            return "Ich konnte die Datei nicht erkennen."

        if new_name is None:
            return "Ich konnte den neuen Dateinamen nicht erkennen."

        source = self._find_source(source_name)

        if source is None:
            return f"Ich konnte '{source_name}' nicht finden."

        if FileActions.rename_file(source, new_name):
            return (
                f"Ich habe '{source.name}' "
                f"in '{new_name}' umbenannt."
            )

        return f"'{source.name}' konnte nicht umbenannt werden."

    def _parse_command(
        self,
        prompt: str,
    ) -> tuple[str | None, str | None]:
        text = prompt.lower().strip()

        commands = (
            "benenne ",
            "benenn ",
            "umbenennen ",
            "rename ",
        )

        for command in commands:
            if text.startswith(command):
                text = text[len(command):]
                break

        # "Benenne test.txt um in neuer.txt"
        # wird zuerst in Quelle und Ziel getrennt.
        markers = (
            " um in ",
            " in ",
            " zu ",
            " als ",
        )

        source_name = None
        new_name = None

        for marker in markers:
            if marker in text:
                parts = text.split(marker, 1)

                source_name = parts[0].strip()
                new_name = parts[1].strip()

                break

        if source_name is None or new_name is None:
            return None, None

        source_name = source_name.strip(" .,!?")
        new_name = new_name.strip(" .,!?")

        if new_name.endswith(" bitte"):
            new_name = new_name[:-6].strip()

        if not source_name or not new_name:
            return None, None

        return source_name, new_name

    def _find_source(self, source_name: str) -> Path | None:
        """Sucht die Quelldatei in bekannten Benutzerordnern."""

        home = Path.home()

        folders = (
            home / "Downloads",
            home / "Documents",
            home / "Desktop",
            home / "Pictures",
            home / "Videos",
            home / "Music",
        )

        search_name = source_name.lower().strip()

        for folder in folders:
            if not folder.exists():
                continue

            try:
                for path in folder.rglob("*"):
                    if path.name.lower() == search_name:
                        return path

            except OSError:
                continue

        return None