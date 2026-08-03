from __future__ import annotations

from abc import ABC, abstractmethod


class Plugin(ABC):
    """Basisklasse für alle Plugins."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Name des Plugins."""
        raise NotImplementedError

    @abstractmethod
    def load(self) -> None:
        """Wird beim Laden des Plugins aufgerufen."""
        raise NotImplementedError

    @abstractmethod
    def unload(self) -> None:
        """Wird beim Entladen des Plugins aufgerufen."""
        raise NotImplementedError