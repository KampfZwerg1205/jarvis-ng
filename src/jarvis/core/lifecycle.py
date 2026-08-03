from __future__ import annotations

from collections.abc import Callable


class LifecycleManager:
    """Verwaltet Start- und Stop-Aufgaben."""

    def __init__(self) -> None:
        self._startup_tasks: list[Callable[[], None]] = []
        self._shutdown_tasks: list[Callable[[], None]] = []

    def add_startup_task(self, task: Callable[[], None]) -> None:
        self._startup_tasks.append(task)

    def add_shutdown_task(self, task: Callable[[], None]) -> None:
        self._shutdown_tasks.append(task)

    def startup(self) -> None:
        for task in self._startup_tasks:
            task()

    def shutdown(self) -> None:
        for task in reversed(self._shutdown_tasks):
            task()