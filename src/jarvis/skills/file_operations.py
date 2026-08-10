from __future__ import annotations

from pathlib import Path

from jarvis.skills.base import Skill
from jarvis.system.file_actions import FileActions


class FileOperationsSkill(Skill):
    """Kopiert und verschiebt Dateien in bekannten Windows-Ordnern."""

    @property
    def name(self) -> str:
        return "file_operations"

    def can_handle(self, prompt: str) -> bool:
        prompt = prompt.lower().strip()

        commands = (
            "kopiere ",
            "kopier ",
            "verschiebe ",
            "verschieb ",
        )

        folders = (
            "downloads",
            "dokumente",
            "desktop",
            "bilder",
            "videos",
            "musik",
        )

        return (
            any(prompt.startswith(command) for command in commands)
            and any(folder in prompt for folder in folders)
        )

    def confidence(self, prompt: str) -> float:
        if self.can_handle(prompt):
            return 1.0

        return 0.0

    def execute(self, prompt: str) -> str:
        prompt = prompt.lower().strip()

        source_name, destination_folder = self._parse_command(prompt)

        if source_name is None:
            return "Ich konnte die Quelldatei nicht erkennen."

        if destination_folder is None:
            return "Ich konnte den Zielordner nicht erkennen."

        source = self._find_source(source_name)

        if source is None:
            return f"Ich konnte '{source_name}' nicht finden."

        destination = destination_folder / source.name

        try:
            if source.resolve() == destination.resolve():
                return "Quelle und Ziel sind identisch."

        except OSError:
            return "Quelle und Ziel konnten nicht geprüft werden."

        if prompt.startswith(("kopiere ", "kopier ")):
            if FileActions.copy_file(source, destination):
                return (
                    f"Ich habe '{source.name}' nach "
                    f"{destination_folder.name} kopiert."
                )

            return f"'{source.name}' konnte nicht kopiert werden."

        if prompt.startswith(("verschiebe ", "verschieb ")):
            if FileActions.move_file(source, destination):
                return (
                    f"Ich habe '{source.name}' nach "
                    f"{destination_folder.name} verschoben."
                )

            return f"'{source.name}' konnte nicht verschoben werden."

        return "Diese Dateioperation wird noch nicht unterstützt."

    def _parse_command(
        self,
        prompt: str,
    ) -> tuple[str | None, Path | None]:
        # Für die Verarbeitung wird alles vereinheitlicht.
        text = prompt.lower().strip()

        commands = (
            "kopiere ",
            "kopier ",
            "verschiebe ",
            "verschieb ",
        )

        for command in commands:
            if text.startswith(command):
                text = text[len(command):]
                break

        folders = {
            "downloads": Path.home() / "Downloads",
            "dokumente": Path.home() / "Documents",
            "desktop": Path.home() / "Desktop",
            "bilder": Path.home() / "Pictures",
            "videos": Path.home() / "Videos",
            "musik": Path.home() / "Music",
        }

        destination_path = None

        for name, path in folders.items():
            markers = (
                f" nach {name}",
                f" in {name}",
                f" auf {name}",
                f" nach dem {name}",
                f" in den {name}",
                f" auf dem {name}",
            )

            for marker in markers:
                if marker in text:
                    destination_path = path
                    text = text.replace(marker, "")
                    break

            if destination_path is not None:
                break

        text = text.strip(" .,!?")

        if text.endswith(" bitte"):
            text = text[:-6].strip()

        if not text:
            return None, destination_path

        return text, destination_path

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