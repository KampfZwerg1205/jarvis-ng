from __future__ import annotations

from jarvis.ai.provider import AIProvider
from jarvis.core.config import settings


class AIRouter:
    """Verwaltet KI-Provider und Fallbacks."""

    def __init__(self) -> None:
        self._providers: dict[str, AIProvider] = {}

    def register(self, provider: AIProvider) -> None:
        self._providers[provider.name] = provider

    def get(self, name: str | None = None) -> AIProvider:
        if name is None:
            name = settings.ai_provider

        if name not in self._providers:
            raise ValueError(
                f"KI-Provider '{name}' ist nicht registriert."
            )

        return self._providers[name]

    def chat(
        self,
        prompt: str,
        provider: str | None = None,
    ) -> str:

        primary = provider or settings.ai_provider

        providers = [
            primary,
            *[
                name
                for name in self._providers
                if name != primary
            ],
        ]

        last_error: Exception | None = None

        for name in providers:
            try:
                return self.get(name).chat(prompt)

            except Exception as exc:
                last_error = exc

        raise RuntimeError(
            "Kein KI-Provider verfügbar."
        ) from last_error