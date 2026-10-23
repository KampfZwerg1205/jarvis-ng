from pathlib import Path
from unittest.mock import patch

from jarvis.skills.file_search import FileSearchSkill


def test_file_search_detects_downloads() -> None:
    skill = FileSearchSkill()

    assert skill.can_handle("Finde rechnung.pdf in Downloads")


def test_file_search_detects_desktop() -> None:
    skill = FileSearchSkill()

    assert skill.can_handle("Suche bild.png auf Desktop")


def test_file_search_detects_global_file_search() -> None:
    skill = FileSearchSkill()
    assert skill.can_handle("Finde rechnung.pdf")
    assert skill.can_handle("Suche die Rechnung auf meinem PC")
    assert not skill.can_handle("Finde heraus, wie das funktioniert")


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


def test_file_search_extracts_global_search_phrase() -> None:
    assert FileSearchSkill()._extract_search_name(
        "Suche die Rechnung auf meinem PC"
    ) == "rechnung"


def test_file_search_searches_all_configured_roots(tmp_path: Path) -> None:
    file_path = tmp_path / "Projects" / "rechnung.pdf"
    file_path.parent.mkdir()
    file_path.write_text("test", encoding="utf-8")
    skill = FileSearchSkill()

    with patch.object(skill, "_search_roots", return_value=(tmp_path,)):
        response = skill.execute("Finde rechnung.pdf")

    assert "1 Treffer auf deinem PC" in response
    assert str(file_path) in response


def test_file_search_keeps_known_folder_search_scoped(tmp_path: Path) -> None:
    file_path = tmp_path / "rechnung.pdf"
    file_path.write_text("test", encoding="utf-8")
    skill = FileSearchSkill()

    with (
        patch.object(skill, "_find_folder", return_value=tmp_path),
        patch.object(skill, "_search_roots") as search_roots,
    ):
        response = skill.execute("Finde rechnung.pdf in Downloads")

    assert "1 Treffer in" in response
    assert "rechnung.pdf" in response
    search_roots.assert_not_called()
