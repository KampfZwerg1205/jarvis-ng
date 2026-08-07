from __future__ import annotations

import requests

from jarvis.ai.provider import AIProvider
from jarvis.core.config import settings


class OllamaProvider(AIProvider):
    """Lokaler KI-Provider über Ollama."""

    @property
    def name(self) -> str:
        return "ollama"

    def chat(self, prompt: str) -> str:
        response = requests.post(
            f"{settings.ollama_host}/api/generate",
            json={
                "model": "llama3.2",
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )

        response.raise_for_status()

        data = response.json()

        return data.get(
            "response",
            "",
        )