from jarvis.core.config import settings
from jarvis.core.container import ServiceContainer
from jarvis.core.events import EventBus
from jarvis.core.lifecycle import LifecycleManager
from jarvis.core.logger import get_logger


class JarvisApp:
    def __init__(self) -> None:
        self.container = ServiceContainer()

        self.container.register("logger", get_logger())
        self.container.register("settings", settings)
        self.container.register("events", EventBus())

        self.lifecycle = LifecycleManager()

        self.lifecycle.add_startup_task(self._on_start)
        self.lifecycle.add_shutdown_task(self._on_stop)

    @property
    def logger(self):
        return self.container.get("logger")

    @property
    def events(self):
        return self.container.get("events")

    def _on_start(self) -> None:
        self.logger.info(
            f"{settings.app_name} {settings.version} wird gestartet."
        )
        self.events.publish("app.started")

    def _on_stop(self) -> None:
        self.events.publish("app.stopped")
        self.logger.info("JARVIS wurde beendet.")

    def start(self) -> None:
        self.lifecycle.startup()

    def stop(self) -> None:
        self.lifecycle.shutdown()