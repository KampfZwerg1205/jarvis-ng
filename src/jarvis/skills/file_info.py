from __future__ import annotations

from pathlib import Path

from jarvis.skills.base import Skill


class FileInfoSkill(Skill):
    """Liefert Informationen über bekannte Windows-Ordner."""

    MAX_ITEMS = 10

    @property
    def name(self) -> str:
        return "file_info"

    def can_handle(self, prompt: str) -> bool:
        prompt = prompt.lower().strip()

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

        folder = self._find_folder(prompt)

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

        if self._should_list_files(prompt):
            response += self._format_file_list(files)

        # ---------------------------------------------------------
        # ORDNER AUFLISTEN
        # ---------------------------------------------------------

        if self._should_list_directories(prompt):
            response += self._format_directory_list(directories)

        return response

    def _find_folder(self, prompt: str) -> Path | None:
        home = Path.home()

        folders = {
            "downloads": home / "Downloads",
            "dokumente": home / "Documents",
            "desktop": home / "Desktop",
            "bilder": home / "Pictures",
            "videos": home / "Videos",
            "musik": home / "Music",
        }

        for name, path in folders.items():
            if name in prompt:
                return path

        return None

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