from jarvis.core.container import ServiceContainer


def test_register_service() -> None:
    container = ServiceContainer()

    service = object()

    container.register("service", service)

    assert container.has("service")
    assert container.get("service") is service