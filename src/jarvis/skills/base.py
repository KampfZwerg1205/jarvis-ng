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

    def confidence(self, prompt: str) -> float:
        """
        Gibt die Sicherheit zurück, dass dieser Skill zuständig ist.

        Wert zwischen 0.0 und 1.0
        """
        if self.can_handle(prompt):
            return 0.5

        return 0.0