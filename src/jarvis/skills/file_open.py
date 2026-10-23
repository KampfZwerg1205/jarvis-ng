from __future__ import annotations

from pathlib import Path

from jarvis.skills.base import Skill
from jarvis.system.file_actions import FileActions


class FileOpenSkill(Skill):
    """Sucht eine Datei in bekannten Benutzerordnern und öffnet sie."""

    FOLDERS = {
        "downloads": "Downloads",
        "dokumente": "Documents",
        "desktop": "Desktop",
        "bilder": "Pictures",
        "videos": "Videos",
        "musik": "Music",
    }

    FOLDER_SUFFIXES = (
        (" auf dem desktop", "desktop"),
        (" auf desktop", "desktop"),
        (" im downloads-ordner", "downloads"),
        (" im download-ordner", "downloads"),
        (" in downloads", "downloads"),
        (" im dokumente-ordner", "dokumente"),
        (" in den dokumenten", "dokumente"),
        (" in dokumente", "dokumente"),
        (" im bilder-ordner", "bilder"),
        (" in den bildern", "bilder"),
        (" in bilder", "bilder"),
        (" im videos-ordner", "videos"),
        (" in videos", "videos"),
        (" im musik-ordner", "musik"),
        (" in der musik", "musik"),
        (" in musik", "musik"),
    )

    @property
    def name(self) -> str:
        return "file_open"

    def can_handle(self, prompt: str) -> bool:
        return self._parse_command_details(prompt) is not None

    def confidence(self, prompt: str) -> float:
        return 1.0 if self.can_handle(prompt) else 0.0

    def execute(self, prompt: str) -> str:
        details = self._parse_command_details(prompt)
        if details is None:
            return "Ich konnte keinen Dateinamen erkennen."

        filename, folder_name = details

        if folder_name is None:
            source = self._find_source(filename)
        else:
            source = self._find_source(filename, Path.home() / self.FOLDERS[folder_name])
        if source is None:
            return f"Ich konnte '{filename}' nicht finden."

        if FileActions.open_path(source):
            return f"Ich öffne '{source.name}'."
        return f"'{source.name}' konnte nicht geöffnet werden."

    def _parse_command(self, prompt: str) -> str | None:
        details = self._parse_command_details(prompt)
        return details[0] if details is not None else None

    def _parse_command_details(self, prompt: str) -> tuple[str, str | None] | None:
        text = prompt.lower().strip()
        commands = ("öffne die datei ", "oeffne die datei ", "öffne ", "oeffne ", "mach auf ", "mach ")
        for command in commands:
            if text.startswith(command):
                text = text[len(command):]
                break
        else:
            return None

        folder_name = None
        for suffix, name in self.FOLDER_SUFFIXES:
            if text.endswith(suffix):
                text = text[:-len(suffix)]
                folder_name = name
                break

        for prefix in ("die datei ", "datei ", "die ", "den ", "das ", "bitte "):
            if text.startswith(prefix):
                text = text[len(prefix):]
                break
        text = text.strip(" .,!?\"'")
        if text.endswith(" bitte"):
            text = text[:-6].strip()
        if (
            not text
            or Path(text).name != text
            or text in self.FOLDERS
            or text.startswith("ordner ")
            or text in ("papierkorb", "mülleimer")
        ):
            return None
        return text, folder_name

    def _find_source(self, filename: str, folder: Path | None = None) -> Path | None:
        home = Path.home()
        folders = (folder,) if folder is not None else tuple(
            home / path for path in self.FOLDERS.values()
        )
        for folder in folders:
            if not folder.exists():
                continue
            try:
                for path in folder.rglob("*"):
                    if path.is_file() and path.name.lower() == filename.lower():
                        return path
            except OSError:
                continue
        return None
