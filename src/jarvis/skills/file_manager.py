from __future__ import annotations

import re
from pathlib import Path

from jarvis.skills.base import Skill
from jarvis.system.file_actions import FileActions
from jarvis.system.folder_search import find_folders_by_name, local_search_roots


class FileManagerSkill(Skill):
    """Öffnet bekannte Dateien und Windows-Ordner."""

    USER_FOLDERS = {
        "downloads": "Downloads",
        "dokumente": "Documents",
        "desktop": "Desktop",
        "bilder": "Pictures",
        "videos": "Videos",
        "musik": "Music",
    }

    SUBFOLDER_COMMAND = re.compile(
        r"^(?:öffne|oeffne|mach(?: auf)?)\s+"
        r"(?:bitte\s+)?(?:den\s+)?ordner\s+(.+?)"
        r"(?:\s+(?:auf dem|auf|im|in)\s+"
        r"(desktop|downloads|dokumente|bilder|videos|musik))?"
        r"[.!?]*$",
        re.IGNORECASE,
    )

    @property
    def name(self) -> str:
        return "file_manager"

    def can_handle(self, prompt: str) -> bool:
        prompt = prompt.lower().strip()

        if self._parse_subfolder_command(prompt) is not None:
            return True
        if "ordner" in prompt and prompt.startswith(("öffne ", "oeffne ", "mach ")):
            return False

        commands = (
            # Öffnen
            "öffne ",
            "zeige mir ",
            "mach ",
            "mach auf ",

            # Bekannte Ordner
            "downloads",
            "dokumente",
            "desktop",
            "bilder",
            "videos",
            "musik",
            "papierkorb",
        )

        # Wir wollen nicht jedes beliebige "mach" abfangen.
        folder_names = (
            "downloads",
            "dokumente",
            "desktop",
            "bilder",
            "videos",
            "musik",
            "papierkorb",
        )

        open_commands = (
            "öffne ",
            "zeige mir ",
            "mach ",
            "mach auf ",
        )

        return (
            any(command in prompt for command in open_commands)
            and any(folder in prompt for folder in folder_names)
        )

    def confidence(self, prompt: str) -> float:
        if self.can_handle(prompt):
            return 1.0

        return 0.0

    def execute(self, prompt: str) -> str:
        prompt = prompt.lower().strip()

        subfolder = self._parse_subfolder_command(prompt)
        if subfolder is not None:
            folder_name, parent_name = subfolder
            if parent_name is not None:
                parent = Path.home() / self.USER_FOLDERS[parent_name]
                matches = [parent / folder_name]
            elif folder_name in self.USER_FOLDERS:
                matches = [Path.home() / self.USER_FOLDERS[folder_name]]
            else:
                matches = self._find_matching_folders(folder_name)

            if not matches:
                return f"Ich konnte keinen Ordner namens '{folder_name}' finden."
            if len(matches) > 1:
                return self._format_folder_matches(folder_name, matches)
            folder = matches[0]

            if not folder.is_dir():
                return f"Der Ordner '{folder_name}' wurde nicht gefunden."

            if FileActions.open_path(folder):
                return f"Ich öffne den Ordner '{folder_name}'."

            return f"Der Ordner '{folder_name}' konnte nicht geöffnet werden."

        # ---------------------------------------------------------
        # DOWNLOADS
        # ---------------------------------------------------------

        if "downloads" in prompt:
            if FileActions.open_downloads():
                return "Ich öffne den Downloads-Ordner."

            return "Der Downloads-Ordner konnte nicht geöffnet werden."

        # ---------------------------------------------------------
        # DOKUMENTE
        # ---------------------------------------------------------

        if "dokumente" in prompt:
            if FileActions.open_documents():
                return "Ich öffne den Dokumente-Ordner."

            return "Der Dokumente-Ordner konnte nicht geöffnet werden."

        # ---------------------------------------------------------
        # DESKTOP
        # ---------------------------------------------------------

        if "desktop" in prompt:
            if FileActions.open_desktop():
                return "Ich öffne den Desktop."

            return "Der Desktop konnte nicht geöffnet werden."

        # ---------------------------------------------------------
        # BILDER
        # ---------------------------------------------------------

        if "bilder" in prompt:
            if FileActions.open_pictures():
                return "Ich öffne den Bilder-Ordner."

            return "Der Bilder-Ordner konnte nicht geöffnet werden."

        # ---------------------------------------------------------
        # VIDEOS
        # ---------------------------------------------------------

        if "videos" in prompt:
            if FileActions.open_videos():
                return "Ich öffne den Videos-Ordner."

            return "Der Videos-Ordner konnte nicht geöffnet werden."

        # ---------------------------------------------------------
        # MUSIK
        # ---------------------------------------------------------

        if "musik" in prompt:
            if FileActions.open_music():
                return "Ich öffne den Musik-Ordner."

            return "Der Musik-Ordner konnte nicht geöffnet werden."

        # ---------------------------------------------------------
        # PAPIERKORB
        # ---------------------------------------------------------

        if "papierkorb" in prompt:
            if FileActions.open_recycle_bin():
                return "Ich öffne den Papierkorb."

            return "Der Papierkorb konnte nicht geöffnet werden."

        return "Dieser Datei- oder Ordnerbefehl wird noch nicht unterstützt."

    def _parse_subfolder_command(self, prompt: str) -> tuple[str, str | None] | None:
        match = self.SUBFOLDER_COMMAND.fullmatch(prompt.strip())
        if match is None:
            return None

        folder_name = match.group(1).strip().strip("\"'")
        parent_name = match.group(2)
        invalid_windows_chars = '<>:"/\\|?*'
        if (
            not folder_name
            or folder_name in (".", "..")
            or any(char in invalid_windows_chars for char in folder_name)
            or folder_name.endswith((" ", "."))
        ):
            return None

        return folder_name, parent_name.lower() if parent_name else None

    def _find_matching_folders(self, folder_name: str) -> list[Path]:
        return find_folders_by_name(folder_name, local_search_roots())

    def _format_folder_matches(self, folder_name: str, matches: list[Path]) -> str:
        visible_matches = matches[:5]
        response = (
            f"Ich habe mehrere Ordner namens '{folder_name}' gefunden. "
            "Bitte gib den gewünschten Speicherort an:\n- "
            + "\n- ".join(str(path) for path in visible_matches)
        )
        if len(matches) > len(visible_matches):
            response += "\nWeitere Treffer wurden nicht angezeigt."
        return response
