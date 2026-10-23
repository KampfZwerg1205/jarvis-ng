from __future__ import annotations

import re
from pathlib import Path

from jarvis.skills.base import Skill
from jarvis.system.folder_search import find_paths_by_name, local_search_roots


class FileSearchSkill(Skill):
    """Sucht Dateien und Ordner auf dem PC oder in bekannten Ordnern."""

    MAX_RESULTS = 10

    @property
    def name(self) -> str:
        return "file_search"

    def can_handle(self, prompt: str) -> bool:
        prompt = prompt.lower().strip()

        commands = (
            "finde ",
            "suche ",
            "such ",
            "wo ist ",
            "wo liegt ",
            "wo befindet sich ",
            "findest du ",
            "kannst du ",
        )

        folders = (
            "downloads",
            "dokumente",
            "desktop",
            "bilder",
            "videos",
            "musik",
        )

        if not any(prompt.startswith(command) for command in commands):
            return False

        search_name = self._extract_search_name(prompt)
        if not search_name or prompt.startswith("finde heraus "):
            return False

        global_locations = (
            " auf meinem pc",
            " auf dem pc",
            " auf meinem computer",
            " auf dem computer",
            " auf allen laufwerken",
        )
        has_file_hint = (
            any(folder in prompt for folder in folders)
            or any(location in prompt for location in global_locations)
            or "datei" in prompt
            or re.search(r"\.[a-z0-9]{1,10}$", search_name) is not None
        )
        return has_file_hint

    def confidence(self, prompt: str) -> float:
        if self.can_handle(prompt):
            return 1.0

        return 0.0

    def execute(self, prompt: str) -> str:
        prompt = prompt.lower().strip()

        folder = self._find_folder(prompt)
        if folder is not None and not folder.exists():
            return f"Der Ordner {folder.name} wurde nicht gefunden."

        search_name = self._extract_search_name(prompt)

        if not search_name:
            return "Ich konnte keinen Dateinamen erkennen."

        roots = (folder,) if folder is not None else self._search_roots()
        matches = self._search(roots, search_name)

        if not matches:
            if folder is None:
                return f"Ich konnte '{search_name}' auf deinem PC nicht finden."
            return f"Ich konnte '{search_name}' in {folder.name} nicht finden."

        visible_matches = matches[:self.MAX_RESULTS]

        if folder is None:
            result_names = [str(match) for match in visible_matches]
            response = (
                f"Ich habe {len(matches)} Treffer auf deinem PC gefunden:\n"
            )
        else:
            result_names = [str(match.relative_to(folder)) for match in visible_matches]
            response = f"Ich habe {len(matches)} Treffer in {folder.name} gefunden:\n"

        response += "\n".join(f"- {name}" for name in result_names)

        if len(matches) > self.MAX_RESULTS:
            remaining = len(matches) - self.MAX_RESULTS
            response += (
                f"\n- ... und {remaining} weitere Treffer."
            )

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

    def _extract_search_name(self, prompt: str) -> str | None:
        text = prompt.lower().strip()

        # ---------------------------------------------------------
        # BEFEHL ENTFERNEN
        # ---------------------------------------------------------

        commands = (
            "finde ",
            "suche ",
            "such ",
            "wo ist ",
            "wo liegt ",
            "wo befindet sich ",
            "findest du ",
            "kannst du ",
        )

        for command in commands:
            if text.startswith(command):
                text = text[len(command):]
                break

        # ---------------------------------------------------------
        # HILFSWÖRTER ENTFERNEN
        # ---------------------------------------------------------

        prefixes = (
            "nach ",
            "meine ",
            "meinen ",
            "mein ",
            "meiner ",
            "meinem ",
            "die ",
            "der ",
            "das ",
            "den ",
            "eine ",
            "einen ",
            "ein ",
        )

        changed = True

        while changed:
            changed = False

            for prefix in prefixes:
                if text.startswith(prefix):
                    text = text[len(prefix):].strip()
                    changed = True
                    break

        # ---------------------------------------------------------
        # ORDNER AUS DEM SUCHTEXT ENTFERNEN
        # ---------------------------------------------------------

        folders = (
            "downloads",
            "dokumente",
            "desktop",
            "bilder",
            "videos",
            "musik",
        )

        for folder in folders:
            text = text.replace(
                f" in {folder}",
                "",
            )

            text = text.replace(
                f" auf {folder}",
                "",
            )

            text = text.replace(
                f" im {folder}",
                "",
            )

            text = text.replace(
                f" auf dem {folder}",
                "",
            )

            text = text.replace(
                f" in den {folder}",
                "",
            )

            text = text.replace(
                f" in die {folder}",
                "",
            )

        for location in (
            " auf meinem pc",
            " auf dem pc",
            " auf meinem computer",
            " auf dem computer",
            " auf allen laufwerken",
        ):
            text = text.replace(location, "")

        # ---------------------------------------------------------
        # FRAGEZEICHEN UND SATZZEICHEN ENTFERNEN
        # ---------------------------------------------------------

        text = text.strip(" .,!?")

        # ---------------------------------------------------------
        # NACHGESTELLTE WÖRTER ENTFERNEN
        # ---------------------------------------------------------

        endings = (
            " bitte",
            " suchen",
            " finden",
            " heraus",
        )

        changed = True

        while changed:
            changed = False

            for ending in endings:
                if text.endswith(ending):
                    text = text[:-len(ending)].strip()
                    changed = True

        # ---------------------------------------------------------
        # ERNEUT BEREINIGEN
        # ---------------------------------------------------------

        text = text.strip(" .,!?")

        return text if text else None

    def _search(
        self,
        roots: tuple[Path, ...],
        search_name: str,
    ) -> list[Path]:
        return find_paths_by_name(search_name, roots, max_results=100)

    def _search_roots(self) -> tuple[Path, ...]:
        return local_search_roots()
