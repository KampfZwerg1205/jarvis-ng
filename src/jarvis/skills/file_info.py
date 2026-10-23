from __future__ import annotations

import re
from pathlib import Path

from jarvis.skills.base import Skill
from jarvis.system.folder_search import find_folders_by_name, local_search_roots


class FileInfoSkill(Skill):
    """Liefert Informationen über bekannte Windows-Ordner."""

    MAX_ITEMS = 10
    USER_FOLDERS = {
        "downloads": "Downloads",
        "dokumente": "Documents",
        "desktop": "Desktop",
        "bilder": "Pictures",
        "videos": "Videos",
        "musik": "Music",
    }
    SUBFOLDER_QUERY = re.compile(
        r"^(?:was ist|was befindet sich|was liegt)\s+"
        r"(?:im|in dem|in der|in den)\s+(?:ordner\s+)?(.+?)"
        r"(?:\s+(?:auf dem|auf|im|in)\s+"
        r"(desktop|downloads|dokumente|bilder|videos|musik))?"
        r"[.!?]*$",
        re.IGNORECASE,
    )

    @property
    def name(self) -> str:
        return "file_info"

    def can_handle(self, prompt: str) -> bool:
        prompt = prompt.lower().strip()

        if "ordner" in prompt:
            return self._parse_subfolder_query(prompt) is not None

        questions = (
            "was ist in",
            "was befindet sich in",
            "was befindet sich auf",
            "was liegt in",
            "was liegt auf",
            "zeige mir den inhalt",
            "wie viele dateien",
            "wie viele ordner",
            "inhalt von",
            "welche dateien",
            "welche ordner",
            "zeige die dateien",
            "zeige die ordner",
            "liste die dateien",
            "liste die ordner",
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
            any(question in prompt for question in questions)
            and any(folder in prompt for folder in folders)
        )

    def confidence(self, prompt: str) -> float:
        if self.can_handle(prompt):
            return 1.0

        return 0.0

    def execute(self, prompt: str) -> str:
        prompt = prompt.lower().strip()

        subfolder = self._parse_subfolder_query(prompt)
        if subfolder is None:
            folder = self._find_folder(prompt)
        else:
            folder_name, parent_name = subfolder
            if parent_name is not None:
                folder = Path.home() / self.USER_FOLDERS[parent_name] / folder_name
            else:
                matches = self._find_matching_folders(folder_name)
                if not matches:
                    return f"Ich konnte keinen Ordner namens '{folder_name}' finden."
                if len(matches) > 1:
                    return self._format_folder_matches(folder_name, matches)
                folder = matches[0]

        if folder is None:
            return "Diesen Ordner kann ich momentan nicht auswerten."

        if not folder.exists():
            return f"Der Ordner {folder.name} wurde nicht gefunden."

        try:
            entries = list(folder.iterdir())
        except OSError:
            return "Auf diesen Ordner konnte nicht zugegriffen werden."

        files = [
            entry
            for entry in entries
            if entry.is_file()
        ]

        directories = [
            entry
            for entry in entries
            if entry.is_dir()
        ]

        response = (
            f"In {folder.name} befinden sich "
            f"{len(files)} Dateien und "
            f"{len(directories)} Ordner."
        )

        # ---------------------------------------------------------
        # DATEIEN AUFLISTEN
        # ---------------------------------------------------------

        if subfolder is not None or self._should_list_files(prompt):
            response += self._format_file_list(files)

        # ---------------------------------------------------------
        # ORDNER AUFLISTEN
        # ---------------------------------------------------------

        if subfolder is not None or self._should_list_directories(prompt):
            response += self._format_directory_list(directories)

        return response

    def _find_folder(self, prompt: str) -> Path | None:
        home = Path.home()

        folders = {
            name: home / path
            for name, path in self.USER_FOLDERS.items()
        }

        for name, path in folders.items():
            if name in prompt:
                return path

        return None

    def _parse_subfolder_query(self, prompt: str) -> tuple[str, str | None] | None:
        match = self.SUBFOLDER_QUERY.fullmatch(prompt.strip())
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
        return find_folders_by_name(folder_name, self._search_roots())

    def _search_roots(self) -> tuple[Path, ...]:
        return local_search_roots()

    def _format_folder_matches(self, folder_name: str, matches: list[Path]) -> str:
        visible_matches = matches[:5]
        result = (
            f"Ich habe mehrere Ordner namens '{folder_name}' gefunden. "
            "Bitte gib den gewünschten Speicherort an:\n- "
            + "\n- ".join(str(path) for path in visible_matches)
        )
        if len(matches) > len(visible_matches):
            result += "\nWeitere Treffer wurden nicht angezeigt."
        return result

    def _should_list_files(self, prompt: str) -> bool:
        commands = (
            "was ist in",
            "was befindet sich in",
            "was befindet sich auf",
            "was liegt in",
            "was liegt auf",
            "zeige mir den inhalt",
            "inhalt von",
            "welche dateien",
            "zeige die dateien",
            "liste die dateien",
        )

        return any(command in prompt for command in commands)

    def _should_list_directories(self, prompt: str) -> bool:
        commands = (
            "was ist in",
            "was befindet sich in",
            "was befindet sich auf",
            "was liegt in",
            "was liegt auf",
            "zeige mir den inhalt",
            "inhalt von",
            "welche ordner",
            "zeige die ordner",
            "liste die ordner",
        )

        return any(command in prompt for command in commands)

    def _format_file_list(self, files: list[Path]) -> str:
        if not files:
            return "\nEs befinden sich keine Dateien darin."

        visible_files = files[:self.MAX_ITEMS]

        names = [
            file.name
            for file in visible_files
        ]

        response = "\nDateien: " + ", ".join(names) + "."

        if len(files) > self.MAX_ITEMS:
            remaining = len(files) - self.MAX_ITEMS
            response += (
                f" Weitere {remaining} Dateien werden "
                "nicht angezeigt."
            )

        return response

    def _format_directory_list(
        self,
        directories: list[Path],
    ) -> str:
        if not directories:
            return "\nEs befinden sich keine Unterordner darin."

        visible_directories = directories[:self.MAX_ITEMS]

        names = [
            directory.name
            for directory in visible_directories
        ]

        response = "\nOrdner: " + ", ".join(names) + "."

        if len(directories) > self.MAX_ITEMS:
            remaining = len(directories) - self.MAX_ITEMS
            response += (
                f" Weitere {remaining} Ordner werden "
                "nicht angezeigt."
            )

        return response
