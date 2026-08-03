from __future__ import annotations

from typing import Any


class ServiceContainer:
    """Verwaltet zentrale Dienste."""

    def __init__(self) -> None:
        self._services: dict[str, Any] = {}

    def register(self, name: str, service: Any) -> None:
        """Registriert einen Dienst."""
        self._services[name] = service

    def get(self, name: str) -> Any:
        """Liefert einen registrierten Dienst."""
        try:
            return self._services[name]
        except KeyError as exc:
            raise KeyError(f"Service '{name}' wurde nicht gefunden.") from exc

    def has(self, name: str) -> bool:
        """Prüft, ob ein Dienst existiert."""
        return name in self._services

    def remove(self, name: str) -> None:
        """Entfernt einen Dienst."""
        self._services.pop(name, None)