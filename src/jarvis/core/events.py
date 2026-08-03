from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from typing import Any


class EventBus:
    """Ein einfacher synchroner Event Bus."""

    def __init__(self) -> None:
        self._listeners: dict[str, list[Callable[..., Any]]] = defaultdict(list)

    def subscribe(
        self,
        event_name: str,
        callback: Callable[..., Any],
    ) -> None:
        """Registriert einen Listener."""
        self._listeners[event_name].append(callback)

    def unsubscribe(
        self,
        event_name: str,
        callback: Callable[..., Any],
    ) -> None:
        """Entfernt einen Listener."""
        if callback in self._listeners[event_name]:
            self._listeners[event_name].remove(callback)

    def publish(
        self,
        event_name: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Veröffentlicht ein Event."""
        for callback in list(self._listeners[event_name]):
            callback(*args, **kwargs)