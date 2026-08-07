from __future__ import annotations

from abc import ABC, abstractmethod


class Skill(ABC):
    """Basisklasse für alle JARVIS-Skills."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Eindeutiger Name des Skills."""
        raise NotImplementedError

    @abstractmethod
    def can_handle(self, prompt: str) -> bool:
        """Prüft, ob der Skill die Anfrage verarbeiten kann."""
        raise NotImplementedError

    @abstractmethod
    def execute(self, prompt: str) -> str:
        """Führt den Skill aus."""
        raise NotImplementedError