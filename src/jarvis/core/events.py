from collections import defaultdict
from typing import Any, Callable


class EventBus:
    """Ein einfacher Event Bus."""

    def __init__(self) -> None:
        self._listeners: dict[str, list[Callable[..., None]]] = defaultdict(list)

    def subscribe(self, event_name: str, callback: Callable[..., None]) -> None:
        """Registriert einen Listener."""
        self._listeners[event_name].append(callback)

    def publish(self, event_name: str, *args: Any, **kwargs: Any) -> None:
        """Sendet ein Event an alle Listener."""
        for callback in self._listeners[event_name]:
            callback(*args, **kwargs)