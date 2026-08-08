from __future__ import annotations

from pathlib import Path

from jarvis.skills.base import Skill


class FileInfoSkill(Skill):
    """Liefert Informationen über bekannte Windows-Ordner."""

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

        return (
            f"In {folder.name} befinden sich "
            f"{len(files)} Dateien und "
            f"{len(directories)} Ordner."
        )

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