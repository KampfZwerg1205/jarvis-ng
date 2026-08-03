from jarvis.core.lifecycle import LifecycleManager


def test_lifecycle_order() -> None:
    lifecycle = LifecycleManager()

    result = []

    lifecycle.add_startup_task(lambda: result.append("start"))

    lifecycle.add_shutdown_task(lambda: result.append("stop"))

    lifecycle.startup()
    lifecycle.shutdown()

    assert result == ["start", "stop"]