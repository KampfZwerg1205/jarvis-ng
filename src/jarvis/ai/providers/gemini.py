from jarvis.ai.provider import AIProvider
from jarvis.integrations.gemini_client import GeminiClient


class GeminiProvider(AIProvider):

    @property
    def name(self) -> str:
        return "gemini"

    def __init__(self):
        self.client = GeminiClient()

    def chat(self, prompt: str) -> str:
        return self.client.chat(prompt)