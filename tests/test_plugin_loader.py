from jarvis.core.plugin_loader import PluginLoader
from jarvis.plugins.base import Plugin


class DummyPlugin(Plugin):
    @property
    def name(self) -> str:
        return "dummy"

    def load(self) -> None:
        pass

    def unload(self) -> None:
        pass


def test_register_plugin() -> None:
    loader = PluginLoader()

    plugin = DummyPlugin()

    loader.register(plugin)

    assert loader.get("dummy") is plugin
    assert len(loader.all()) == 1