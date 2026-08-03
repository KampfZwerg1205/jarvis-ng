from __future__ import annotations

from jarvis.ai.provider import AIProvider


class AIRouter:
    """Verwaltet KI-Provider."""

    def __init__(self) -> None:
        self._providers: dict[str, AIProvider] = {}

    def register(self, provider: AIProvider) -> None:
        self._providers[provider.name] = provider

    def get(self, name: str) -> AIProvider:
        return self._providers[name]

    def chat(self, provider: str, prompt: str) -> str:
        return self.get(provider).chat(prompt)