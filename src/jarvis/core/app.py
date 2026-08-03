from jarvis.core.config import settings
from jarvis.core.events import EventBus
from jarvis.core.logger import get_logger


class JarvisApp:
    def __init__(self) -> None:
        self.logger = get_logger()
        self.events = EventBus()

    def start(self) -> None:
        self.logger.info(
            f"{settings.app_name} {settings.version} wird gestartet."
        )

        self.events.publish("app.started")

    def stop(self) -> None:
        self.events.publish("app.stopped")
        self.logger.info("JARVIS wurde beendet.")