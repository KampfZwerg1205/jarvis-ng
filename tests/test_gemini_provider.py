from jarvis.ai.providers.gemini import GeminiProvider


def test_gemini_provider() -> None:
    provider = GeminiProvider()

    result = provider.chat("Hallo")

    assert result == "[Gemini] Hallo"