from __future__ import annotations

from jarvis.ai.provider import AIProvider
from jarvis.core.config import settings


class AIRouter:
    """Verwaltet KI-Provider."""

    def __init__(self) -> None:
        self._providers: dict[str, AIProvider] = {}

    def register(self, provider: AIProvider) -> None:
        self._providers[provider.name] = provider

    def get(self, name: str | None = None) -> AIProvider:
        if name is None:
            name = settings.ai_provider

        if name not in self._providers:
            raise ValueError(f"KI-Provider '{name}' ist nicht registriert.")

        return self._providers[name]

    def chat(self, prompt: str, provider: str | None = None) -> str:
        return self.get(provider).chat(prompt)