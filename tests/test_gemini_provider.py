from unittest.mock import MagicMock, patch

from jarvis.ai.providers import GeminiProvider


@patch("jarvis.ai.providers.gemini.GeminiClient")
def test_provider_creation(mock_client: MagicMock) -> None:
    provider = GeminiProvider()

    assert provider is not None
    assert provider.name == "gemini"
    mock_client.assert_called_once()