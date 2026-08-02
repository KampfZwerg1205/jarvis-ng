from jarvis.core.config import settings
from jarvis.core.logger import get_logger


class JarvisApp:
    def __init__(self):
        self.logger = get_logger()

    def start(self):
        self.logger.info(
            f"{settings.app_name} {settings.version} wird gestartet."
        )

    def stop(self):
        self.logger.info("JARVIS wird beendet.")