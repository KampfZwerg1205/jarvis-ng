from __future__ import annotations

from jarvis.ai.provider import AIProvider


class AIClient:
    """Zentraler Zugriff auf KI-Provider."""

    def __init__(self, provider: AIProvider):
        self.provider = provider

    def chat(self, prompt: str) -> str:
        return self.provider.chat(prompt)