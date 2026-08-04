from jarvis.ai.provider import AIProvider
from jarvis.ai.router import AIRouter


class DummyProvider(AIProvider):

    @property
    def name(self) -> str:
        return "dummy"

    def chat(self, prompt: str) -> str:
        return f"Antwort auf: {prompt}"


def test_router() -> None:
    router = AIRouter()

    router.register(DummyProvider())

    result = router.chat("Hallo", provider="dummy")

    assert result == "Antwort auf: Hallo"