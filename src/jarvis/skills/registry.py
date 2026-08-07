from __future__ import annotations

from jarvis.skills.base import Skill
from jarvis.skills.calculator import CalculatorSkill
from jarvis.skills.time import TimeSkill
from jarvis.skills.system_actions import SystemActionSkill
from jarvis.skills.system_info import SystemInfoSkill
from jarvis.skills.app_launcher import AppLauncherSkill


class SkillRegistry:
    """Zentrale Registrierung der verfügbaren JARVIS-Skills."""

    def __init__(self) -> None:
        self._skills: list[Skill] = []

    def register(self, skill: Skill) -> None:
        self._skills.append(skill)

    def all(self) -> list[Skill]:
        return list(self._skills)

    def load_defaults(self) -> None:
        self.register(TimeSkill())
        self.register(CalculatorSkill())
        self.register(SystemActionSkill())
        self.register(SystemInfoSkill())
        self.register(AppLauncherSkill())