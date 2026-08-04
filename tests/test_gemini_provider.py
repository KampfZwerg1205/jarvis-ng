from jarvis.ai.providers import GeminiProvider


def test_provider_creation() -> None:
    provider = GeminiProvider()

    assert provider is not None