from jarvis.ai.router import AIRouter
from jarvis.ai.provider import AIProvider


class DummyProvider(AIProvider):
    @property
    def name(self) -> str:
        return "gemini"

    def chat(self, prompt: str) -> str:
        return f"Echo: {prompt}"


def test_router_default_provider() -> None:
    router = AIRouter()

    router.register(DummyProvider())

    response = router.chat("Hallo")

    assert response == "Echo: Hallo"