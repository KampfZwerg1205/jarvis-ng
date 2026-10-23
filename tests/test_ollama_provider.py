from unittest.mock import MagicMock, patch

from jarvis.ai.providers.ollama import OllamaProvider
from jarvis.cli.chat import create_ai_router
from jarvis.core.config import Settings, settings


def test_ollama_is_the_default_provider() -> None:
    assert Settings.model_fields["ai_provider"].default == "ollama"


def test_ollama_model_has_local_default() -> None:
    assert Settings.model_fields["ollama_model"].default == "llama3.2"


@patch("jarvis.cli.chat.GeminiProvider")
def test_chat_router_does_not_require_gemini_key(gemini_provider) -> None:
    with (
        patch("jarvis.cli.chat.settings.gemini_api_key", ""),
        patch("jarvis.cli.chat.settings.ai_provider", "ollama"),
    ):
        router = create_ai_router()
        assert router.get().name == "ollama"

    gemini_provider.assert_not_called()


@patch("jarvis.cli.chat.GeminiProvider")
def test_chat_router_does_not_add_cloud_fallback_to_local_mode(
    gemini_provider,
) -> None:
    with (
        patch("jarvis.cli.chat.settings.gemini_api_key", "configured-key"),
        patch("jarvis.cli.chat.settings.ai_provider", "ollama"),
    ):
        router = create_ai_router()

    assert router.get("ollama").name == "ollama"
    gemini_provider.assert_not_called()


@patch("jarvis.ai.providers.ollama.requests.post")
def test_ollama_provider_sends_model_and_system_prompt(post: MagicMock) -> None:
    response = MagicMock()
    response.json.return_value = {"response": "Hallo, Sir."}
    post.return_value = response

    result = OllamaProvider().chat("Sag Hallo")

    assert result == "Hallo, Sir."
    post.assert_called_once_with(
        f"{settings.ollama_host}/api/generate",
        json={
            "model": settings.ollama_model,
            "prompt": "Sag Hallo",
            "system": settings.system_prompt,
            "stream": False,
        },
        timeout=120,
    )
    response.raise_for_status.assert_called_once_with()
