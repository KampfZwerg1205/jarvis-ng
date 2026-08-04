from jarvis.ai.providers.gemini import GeminiProvider


def test_gemini_provider() -> None:
    provider = GeminiProvider("dummy-api-key")

    assert provider.name == "gemini"