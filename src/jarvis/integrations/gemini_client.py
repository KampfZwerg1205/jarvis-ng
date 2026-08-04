from __future__ import annotations

from google import genai

from jarvis.core.config import settings
from jarvis.core.credentials import CredentialManager


class GeminiClient:
    """Client für die Kommunikation mit Google Gemini."""

    def __init__(self) -> None:
        api_key = CredentialManager.get_gemini_api_key()

        if not api_key:
            raise ValueError("Gemini API-Key wurde nicht gefunden.")

        self.client = genai.Client(api_key=api_key)

    def chat(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
        )

        if response.text is None:
            return ""

        return response.text