from jarvis.core.events import EventBus


def test_publish_event() -> None:
    bus = EventBus()

    result = []

    def callback() -> None:
        result.append(True)

    bus.subscribe("test", callback)

    bus.publish("test")

    assert result == [True]