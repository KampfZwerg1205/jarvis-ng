from jarvis.ai.provider import AIProvider


class GeminiProvider(AIProvider):

    def __init__(self, api_key: str):
        self.api_key = api_key

    @property
    def name(self) -> str:
        return "gemini"

    def chat(self, prompt: str) -> str:
        raise NotImplementedError(
            "Gemini API wird im nächsten Sprint implementiert."
        )