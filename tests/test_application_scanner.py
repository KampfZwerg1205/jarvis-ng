from jarvis.system.applications import ApplicationScanner


def test_application_scanner_creation():
    scanner = ApplicationScanner()

    apps = scanner.scan()

    assert isinstance(apps, dict)