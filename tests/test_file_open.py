from pathlib import Path
from unittest.mock import patch

from jarvis.skills.file_open import FileOpenSkill


def test_file_open_detects_file_commands() -> None:
    skill = FileOpenSkill()
    assert skill.can_handle("Öffne test.pdf")
    assert skill.can_handle("Öffne die Datei urlaub.png")
    assert skill.can_handle("Öffne bild.png auf dem Desktop")


def test_file_open_does_not_claim_folder_commands() -> None:
    skill = FileOpenSkill()
    assert not skill.can_handle("Öffne den Desktop")
    assert not skill.can_handle("Öffne den Papierkorb")
    assert not skill.can_handle("Öffne den Ordner kram auf dem Desktop")


def test_file_open_parses_filename() -> None:
    skill = FileOpenSkill()
    assert skill._parse_command("Öffne die Datei urlaub.png") == "urlaub.png"
    assert skill._parse_command("Öffne test.pdf bitte") == "test.pdf"
    assert skill._parse_command("Öffne bild.png auf dem Desktop") == "bild.png"
    assert skill._parse_command("Öffne C:\\Users\\test.pdf") is None


def test_file_open_parses_optional_folder() -> None:
    skill = FileOpenSkill()
    assert skill._parse_command_details("Öffne bild.png auf dem Desktop") == (
        "bild.png",
        "desktop",
    )
    assert skill._parse_command_details("Öffne test.pdf") == ("test.pdf", None)


@patch("jarvis.skills.file_open.FileActions.open_path", return_value=True)
def test_file_open_executes_found_file(mock_open) -> None:
    skill = FileOpenSkill()
    file_path = Path("test.pdf")
    with patch.object(skill, "_find_source", return_value=file_path):
        assert skill.execute("Öffne test.pdf") == "Ich öffne 'test.pdf'."
    mock_open.assert_called_once_with(file_path)


def test_file_open_reports_missing_file() -> None:
    skill = FileOpenSkill()
    with patch.object(skill, "_find_source", return_value=None):
        assert skill.execute("Öffne test.pdf") == "Ich konnte 'test.pdf' nicht finden."


@patch("jarvis.skills.file_open.FileActions.open_path", return_value=True)
def test_file_open_searches_only_in_requested_folder(mock_open) -> None:
    skill = FileOpenSkill()
    file_path = Path.home() / "Desktop" / "bild.png"
    with patch.object(skill, "_find_source", return_value=file_path) as find_source:
        assert skill.execute("Öffne bild.png auf dem Desktop") == "Ich öffne 'bild.png'."

    find_source.assert_called_once_with("bild.png", Path.home() / "Desktop")
    mock_open.assert_called_once_with(file_path)


def test_file_open_does_not_fallback_to_other_folders_when_folder_is_named() -> None:
    skill = FileOpenSkill()
    with patch.object(skill, "_find_source", return_value=None) as find_source:
        assert skill.execute("Öffne bild.png auf dem Desktop") == (
            "Ich konnte 'bild.png' nicht finden."
        )

    find_source.assert_called_once_with("bild.png", Path.home() / "Desktop")
