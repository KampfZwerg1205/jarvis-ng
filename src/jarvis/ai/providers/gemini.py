from __future__ import annotations

from jarvis.ai.provider import AIProvider


class GeminiProvider(AIProvider):
    """Vorläufiger Gemini-Provider."""

    @property
    def name(self) -> str:
        return "gemini"

    def chat(self, prompt: str) -> str:
        # Platzhalter – echte API folgt später
        return f"[Gemini] {prompt}"