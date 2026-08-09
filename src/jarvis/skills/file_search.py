from __future__ import annotations

from pathlib import Path

from jarvis.skills.base import Skill


class FileSearchSkill(Skill):
    """Sucht Dateien und Ordner in bekannten Windows-Ordnern."""

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

        folder = self._find_folder(prompt)

        if folder is None:
            return "Diesen Ordner kann ich momentan nicht durchsuchen."

        if not folder.exists():
            return f"Der Ordner {folder.name} wurde nicht gefunden."

        search_name = self._extract_search_name(prompt)

        if not search_name:
            return "Ich konnte keinen Dateinamen erkennen."

        try:
            matches = self._search(folder, search_name)
        except OSError:
            return "Auf diesen Ordner konnte nicht zugegriffen werden."

        if not matches:
            return (
                f"Ich konnte '{search_name}' "
                f"in {folder.name} nicht finden."
            )

        visible_matches = matches[:self.MAX_RESULTS]

        result_names = [
            str(match.relative_to(folder))
            for match in visible_matches
        ]

        response = (
            f"Ich habe {len(matches)} Treffer in "
            f"{folder.name} gefunden:\n"
            + "\n".join(
                f"- {name}"
                for name in result_names
            )
        )

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
        text = prompt

        commands = (
            "finde ",
            "suche ",
            "such ",
            "wo ist ",
            "wo liegt ",
            "wo befindet sich ",
        )

        for command in commands:
            if text.startswith(command):
                text = text[len(command):]
                break

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

        text = text.strip()

        endings = (
            " bitte",
            " suchen",
        )

        changed = True

        while changed:
            changed = False

            for ending in endings:
                if text.endswith(ending):
                    text = text[:-len(ending)].strip()
                    changed = True

        return text if text else None

    def _search(
        self,
        folder: Path,
        search_name: str,
    ) -> list[Path]:
        search_name = search_name.lower()

        matches: list[Path] = []

        for path in folder.rglob("*"):
            if search_name in path.name.lower():
                matches.append(path)

                if len(matches) >= 100:
                    break

        return matches