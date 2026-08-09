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


def test_file_search_extracts_natural_search() -> None:
    skill = FileSearchSkill()

    assert (
        skill._extract_search_name(
            "Such meine Rechnung in Downloads"
        )
        == "rechnung"
    )


def test_file_search_extracts_search_with_nach() -> None:
    skill = FileSearchSkill()

    assert (
        skill._extract_search_name(
            "Suche nach der Rechnung in Downloads"
        )
        == "rechnung"
    )


def test_file_search_extracts_question() -> None:
    skill = FileSearchSkill()

    assert (
        skill._extract_search_name(
            "Wo befindet sich test.pdf auf dem Desktop?"
        )
        == "test.pdf"
    )