from __future__ import annotations

from jarvis.plugins.base import Plugin


class PluginLoader:
    """Verwaltet geladene Plugins."""

    def __init__(self) -> None:
        self._plugins: dict[str, Plugin] = {}

    def register(self, plugin: Plugin) -> None:
        plugin.load()
        self._plugins[plugin.name] = plugin

    def unregister(self, name: str) -> None:
        plugin = self._plugins.pop(name, None)

        if plugin is not None:
            plugin.unload()

    def get(self, name: str) -> Plugin | None:
        return self._plugins.get(name)

    def all(self) -> list[Plugin]:
        return list(self._plugins.values())