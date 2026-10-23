from pathlib import Path
from unittest.mock import patch

from jarvis.ai.router import AIRouter
from jarvis.conversation.manager import ConversationManager
from jarvis.skills.file_rename import FileRenameSkill


def test_file_rename_detects_benenne() -> None:
    skill = FileRenameSkill()

    assert skill.can_handle(
        "Benenne test.txt in neuer-name.txt"
    )


def test_file_rename_detects_rename() -> None:
    skill = FileRenameSkill()

    assert skill.can_handle(
        "Rename test.txt in neuer-name.txt"
    )


def test_file_rename_ignores_copy() -> None:
    skill = FileRenameSkill()

    assert not skill.can_handle(
        "Kopiere test.txt nach Desktop"
    )


def test_file_rename_parses_command() -> None:
    skill = FileRenameSkill()

    source, new_name = skill._parse_command(
        "Benenne test.txt in neuer-name.txt"
    )

    assert source == "test.txt"
    assert new_name == "neuer-name.txt"


def test_file_rename_parses_um() -> None:
    skill = FileRenameSkill()

    source, new_name = skill._parse_command(
        "Benenne bild.png um in urlaub.png"
    )

    assert source == "bild.png"
    assert new_name == "urlaub.png"


def test_file_rename_parses_absolute_source_without_changing_new_name(
    tmp_path: Path,
) -> None:
    source = tmp_path / "My Files" / "report.pdf"
    skill = FileRenameSkill()

    parsed_source, new_name = skill._parse_command(
        f"Benenne {source} um in Annual Report.PDF"
    )

    assert parsed_source == str(source)
    assert new_name == "Annual Report.PDF"


@patch("jarvis.skills.file_rename.FileActions.rename_file", return_value=True)
def test_file_rename_renames_absolute_source(rename_file, tmp_path: Path) -> None:
    source = tmp_path / "My Files" / "report.pdf"
    source.parent.mkdir()
    source.write_text("report", encoding="utf-8")

    result = FileRenameSkill().execute(
        f"Benenne {source} um in Annual Report.PDF"
    )

    assert result == "Ich habe 'report.pdf' in 'Annual Report.PDF' umbenannt."
    rename_file.assert_called_once_with(source, "Annual Report.PDF")


@patch("jarvis.conversation.manager.FileActions.rename_file", return_value=True)
def test_conversation_confirms_rename_before_renaming(rename_file, tmp_path: Path) -> None:
    source = tmp_path / "Report.pdf"
    source.write_text("report", encoding="utf-8")
    manager = ConversationManager(AIRouter())

    response = manager.chat(f"Benenne {source} um in Annual Report.PDF")

    assert "wirklich" in response
    assert "umbenennen?" in response
    rename_file.assert_not_called()

    result = manager.chat("Ja")

    assert result == "Die Datei wurde umbenannt."
    rename_file.assert_called_once_with(str(source), "Annual Report.PDF")


@patch("jarvis.conversation.manager.FileActions.rename_file")
def test_conversation_can_cancel_rename(rename_file, tmp_path: Path) -> None:
    source = tmp_path / "Report.pdf"
    source.write_text("report", encoding="utf-8")
    manager = ConversationManager(AIRouter())

    manager.chat(f"Benenne {source} um in Annual Report.PDF")
    result = manager.chat("Nein")

    assert result == "Verstanden. Der Vorgang wurde abgebrochen."
    assert manager.pending_action is None
    assert manager.pending_file is None
    assert manager.pending_destination is None
    rename_file.assert_not_called()


@patch("jarvis.conversation.manager.FileActions.rename_file")
def test_conversation_does_not_overwrite_existing_file_on_rename(
    rename_file,
    tmp_path: Path,
) -> None:
    source = tmp_path / "Report.pdf"
    destination = tmp_path / "Annual Report.PDF"
    source.write_text("source", encoding="utf-8")
    destination.write_text("keep this", encoding="utf-8")
    manager = ConversationManager(AIRouter())

    result = manager.chat(f"Benenne {source} um in {destination.name}")

    assert "existiert bereits" in result
    assert manager.pending_action is None
    rename_file.assert_not_called()
