from __future__ import annotations

from jarvis.skills.base import Skill
from jarvis.system.file_actions import FileActions


class FileManagerSkill(Skill):
    """Öffnet bekannte Dateien und Windows-Ordner."""

    @property
    def name(self) -> str:
        return "file_manager"

    def can_handle(self, prompt: str) -> bool:
        prompt = prompt.lower().strip()

        commands = (
            # Downloads
            "öffne downloads",
            "öffne den downloads",

            # Dokumente
            "öffne dokumente",
            "öffne die dokumente",
            "öffne den dokumente",

            # Desktop
            "öffne desktop",
            "öffne den desktop",

            # Bilder
            "öffne bilder",
            "öffne die bilder",

            # Videos
            "öffne videos",
            "öffne die videos",

            # Musik
            "öffne musik",
            "öffne die musik",

            # Papierkorb
            "öffne papierkorb",
            "öffne den papierkorb",
            "öffne den papierkorb auf",
        )

        return any(command in prompt for command in commands)

    def confidence(self, prompt: str) -> float:
        if self.can_handle(prompt):
            return 1.0

        return 0.0

    def execute(self, prompt: str) -> str:
        prompt = prompt.lower().strip()

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