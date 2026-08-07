from __future__ import annotations

import os

from jarvis.skills.base import Skill


class SkillRouter:
    """Verwaltet und findet passende Skills."""

    MIN_CONFIDENCE = 0.7

    def __init__(self) -> None:
        self._skills: list[Skill] = []

        # Debug ist standardmäßig deaktiviert.
        # Zum Aktivieren:
        # $env:JARVIS_DEBUG="1"
        self.debug = os.getenv("JARVIS_DEBUG", "").lower() in (
            "1",
            "true",
            "yes",
            "on",
        )

    def register(self, skill: Skill) -> None:
        self._skills.append(skill)

    def find(self, prompt: str) -> Skill | None:
        best_skill: Skill | None = None
        best_score = 0.0

        for skill in self._skills:
            score = skill.confidence(prompt)

            if self.debug:
                print(f"[DEBUG] {skill.name}: {score}")

            if score > best_score:
                best_score = score
                best_skill = skill

        if best_score < self.MIN_CONFIDENCE:
            return None

        return best_skill

    def execute(self, prompt: str) -> str | None:
        skill = self.find(prompt)

        if skill is None:
            return None

        return skill.execute(prompt)