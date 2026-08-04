from jarvis.core.credentials import CredentialManager


def test_credential_manager() -> None:
    assert isinstance(CredentialManager.get_gemini_api_key(), str)
    assert isinstance(CredentialManager.get_openai_api_key(), str)
    assert isinstance(CredentialManager.get_ollama_host(), str)