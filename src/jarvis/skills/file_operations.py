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
        source, destination = self._parse_command(prompt)
        return source is not None and destination is not None

    def confidence(self, prompt: str) -> float:
        if self.can_handle(prompt):
            return 1.0

        return 0.0

    def execute(self, prompt: str) -> str:
        raw_prompt = prompt.strip()
        prompt = raw_prompt.lower()

        source_name, destination_folder = self._parse_command(raw_prompt)

        if source_name is None:
            return "Ich konnte die Quelldatei nicht erkennen."

        if destination_folder is None:
            return "Ich konnte den Zielordner nicht erkennen."

        source = self._find_source(source_name)

        if source is None:
            return f"Ich konnte '{source_name}' nicht finden."

        if not destination_folder.is_dir():
            return f"Der Zielordner '{destination_folder}' wurde nicht gefunden."

        destination = destination_folder / source.name

        try:
            if source.resolve() == destination.resolve():
                return "Quelle und Ziel sind identisch."

        except OSError:
            return "Quelle und Ziel konnten nicht geprüft werden."

        if destination.exists():
            return f"'{destination.name}' existiert im Zielordner bereits."

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
        text = prompt.strip()
        lowered = text.lower()

        commands = (
            "kopiere ",
            "kopier ",
            "verschiebe ",
            "verschieb ",
        )

        for command in commands:
            if lowered.startswith(command):
                text = text[len(command):]
                lowered = text.lower()
                break
        else:
            return None, None

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
                position = lowered.rfind(marker)
                if position >= 0:
                    destination_path = path
                    text = text[:position]
                    break

            if destination_path is not None:
                break

        if destination_path is None:
            for marker in (" nach ", " in ", " auf "):
                position = lowered.rfind(marker)
                if position < 0:
                    continue
                candidate_text = text[position + len(marker):].strip(
                    " .,!?\"'"
                )
                candidate_path = Path(candidate_text).expanduser()
                if candidate_path.is_absolute():
                    destination_path = candidate_path
                    text = text[:position]
                    break

        text = text.strip(" .,!?\"'")

        if text.lower().endswith(" bitte"):
            text = text[:-6].strip()

        if not text:
            return None, destination_path

        return text, destination_path

    def _find_source(self, source_name: str) -> Path | None:
        """Sucht die Quelldatei in bekannten Benutzerordnern."""

        source_path = Path(source_name).expanduser()
        if source_path.is_absolute():
            return source_path if source_path.is_file() else None

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
