from pathlib import Path
from unittest.mock import patch

from jarvis.skills.file_info import FileInfoSkill


def test_file_info_detects_downloads() -> None:
    skill = FileInfoSkill()

    assert skill.can_handle("Was ist in Downloads")


def test_file_info_detects_desktop() -> None:
    skill = FileInfoSkill()

    assert skill.can_handle("Was befindet sich auf meinem Desktop")


def test_file_info_ignores_unrelated_prompt() -> None:
    skill = FileInfoSkill()

    assert not skill.can_handle("Öffne Discord")


def test_file_info_detects_subfolder_query() -> None:
    assert FileInfoSkill().can_handle(
        "Was ist im Ordner kram auf dem Desktop"
    )
    assert FileInfoSkill().can_handle("Was ist im Ordner kram")


def test_file_info_lists_contents_of_subfolder(tmp_path: Path) -> None:
    folder = tmp_path / "Desktop" / "kram"
    folder.mkdir(parents=True)
    (folder / "notiz.txt").write_text("Text", encoding="utf-8")
    (folder / "bilder").mkdir()

    with patch("jarvis.skills.file_info.Path.home", return_value=tmp_path):
        response = FileInfoSkill().execute(
            "Was ist im Ordner kram auf dem Desktop"
        )

    assert "In kram befinden sich 1 Dateien und 1 Ordner." in response
    assert "Dateien: notiz.txt." in response
    assert "Ordner: bilder." in response


def test_file_info_reports_missing_subfolder(tmp_path: Path) -> None:
    with patch("jarvis.skills.file_info.Path.home", return_value=tmp_path):
        response = FileInfoSkill().execute(
            "Was ist im Ordner kram auf dem Desktop"
        )

    assert response == "Der Ordner kram wurde nicht gefunden."


def test_file_info_finds_folder_without_named_parent(tmp_path: Path) -> None:
    folder = tmp_path / "Projects" / "kram"
    folder.mkdir(parents=True)
    (folder / "notiz.txt").write_text("Text", encoding="utf-8")
    skill = FileInfoSkill()

    with patch.object(skill, "_search_roots", return_value=(tmp_path,)):
        response = skill.execute("Was ist im Ordner kram")

    assert "In kram befinden sich 1 Dateien und 0 Ordner." in response
    assert "Dateien: notiz.txt." in response


def test_file_info_asks_for_location_if_folder_name_is_ambiguous(
    tmp_path: Path,
) -> None:
    first = tmp_path / "Desktop" / "kram"
    second = tmp_path / "Projects" / "kram"
    first.mkdir(parents=True)
    second.mkdir(parents=True)
    skill = FileInfoSkill()

    with patch.object(skill, "_search_roots", return_value=(tmp_path,)):
        response = skill.execute("Was ist im Ordner kram")

    assert "mehrere Ordner namens 'kram'" in response
    assert str(first) in response
    assert str(second) in response


def test_file_info_rejects_path_traversal_in_subfolder_query() -> None:
    assert not FileInfoSkill().can_handle(
        "Was ist im Ordner ..\\Documents auf dem Desktop"
    )
