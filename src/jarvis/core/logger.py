from pathlib import Path
import sys

from loguru import logger

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logger.remove()

logger.add(
    sys.stdout,
    level="INFO",
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> | {message}",
)

logger.add(
    LOG_DIR / "jarvis.log",
    level="DEBUG",
    rotation="10 MB",
    retention="14 days",
    encoding="utf-8",
)


def get_logger():
    """Gibt den zentralen Logger zurück."""
    return logger