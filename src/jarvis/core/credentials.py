from __future__ import annotations

from jarvis.core.config import settings


class CredentialManager:
    """Verwaltet alle Zugangsdaten für externe Dienste."""

    @staticmethod
    def get_gemini_api_key() -> str:
        return settings.gemini_api_key

    @staticmethod
    def get_openai_api_key() -> str:
        return settings.openai_api_key

    @staticmethod
    def get_ollama_host() -> str:
        return settings.ollama_host