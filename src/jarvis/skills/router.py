from __future__ import annotations

from jarvis.skills.base import Skill


class SkillRouter:
    """Verwaltet und findet passende Skills."""

    def __init__(self) -> None:
        self._skills: list[Skill] = []

    def register(self, skill: Skill) -> None:
        self._skills.append(skill)

    def find(self, prompt: str) -> Skill | None:
        for skill in self._skills:
            if skill.can_handle(prompt):
                return skill

        return None

    def execute(self, prompt: str) -> str | None:
        skill = self.find(prompt)

        if skill is None:
            return None

        return skill.execute(prompt)