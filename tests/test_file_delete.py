from pathlib import Path
from unittest.mock import patch

from jarvis.skills.file_delete import FileDeleteSkill


def test_file_delete_handles_delete_command() -> None:
    skill = FileDeleteSkill()

    assert skill.can_handle("Lösche test.pdf")


def test_file_delete_handles_remove_command() -> None:
    skill = FileDeleteSkill()

    assert skill.can_handle("Entferne test.pdf")


def test_file_delete_parses_filename() -> None:
    skill = FileDeleteSkill()

    result = skill._parse_command(
        "Lösche test.pdf"
    )

    assert result == "test.pdf"


def test_file_delete_parses_filename_with_please() -> None:
    skill = FileDeleteSkill()

    result = skill._parse_command(
        "Lösche test.pdf bitte"
    )

    assert result == "test.pdf"


def test_file_delete_requires_filename() -> None:
    skill = FileDeleteSkill()

    result = skill._parse_command(
        "Lösche "
    )

    assert result is None


def test_file_delete_parses_absolute_path_without_changing_case(
    tmp_path: Path,
) -> None:
    file_path = tmp_path / "My Folder" / "Report.PDF"
    result = FileDeleteSkill()._parse_command(f"Lösche {file_path}")

    assert result == str(file_path)


def test_file_delete_finds_file_by_absolute_path(tmp_path: Path) -> None:
    file_path = tmp_path / "My Folder" / "Report.PDF"
    file_path.parent.mkdir()
    file_path.write_text("report", encoding="utf-8")

    assert FileDeleteSkill()._find_source(str(file_path)) == file_path


def test_conversation_still_confirms_delete_by_absolute_path(
    tmp_path: Path,
) -> None:
    from jarvis.ai.router import AIRouter
    from jarvis.conversation.manager import ConversationManager

    file_path = tmp_path / "Report.PDF"
    file_path.write_text("report", encoding="utf-8")
    manager = ConversationManager(AIRouter())

    with patch(
        "jarvis.conversation.manager.FileActions.delete_file",
        return_value=True,
    ) as delete_file:
        response = manager.chat(f"Lösche {file_path}")
        assert "wirklich löschen?" in response
        delete_file.assert_not_called()

        result = manager.chat("Ja")

    assert result == "Die Datei wurde gelöscht."
    delete_file.assert_called_once_with(str(file_path))
