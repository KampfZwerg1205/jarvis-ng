from jarvis.skills.file_search import FileSearchSkill


def test_file_search_detects_downloads() -> None:
    skill = FileSearchSkill()

    assert skill.can_handle("Finde rechnung.pdf in Downloads")


def test_file_search_detects_desktop() -> None:
    skill = FileSearchSkill()

    assert skill.can_handle("Suche bild.png auf Desktop")


def test_file_search_ignores_app_launch() -> None:
    skill = FileSearchSkill()

    assert not skill.can_handle("Öffne Discord")