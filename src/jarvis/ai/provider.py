from __future__ import annotations

from abc import ABC, abstractmethod


class AIProvider(ABC):
    """Basisklasse für alle KI-Provider."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Name des Providers."""
        raise NotImplementedError

    @abstractmethod
    def chat(self, prompt: str) -> str:
        """Verarbeitet eine Chat-Anfrage."""
        raise NotImplementedError