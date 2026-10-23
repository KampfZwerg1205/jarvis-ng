from pathlib import Path
from unittest.mock import patch

from jarvis.ai.router import AIRouter
from jarvis.conversation.manager import ConversationManager
from jarvis.skills.file_operations import FileOperationsSkill
from jarvis.system.file_actions import FileActions


def test_file_operations_detects_copy() -> None:
    skill = FileOperationsSkill()

    assert skill.can_handle(
        "Kopiere test.pdf nach Desktop"
    )


def test_file_operations_detects_move() -> None:
    skill = FileOperationsSkill()

    assert skill.can_handle(
        "Verschiebe test.pdf nach Downloads"
    )


def test_file_operations_ignores_file_search() -> None:
    skill = FileOperationsSkill()

    assert not skill.can_handle(
        "Finde test.pdf in Downloads"
    )


def test_file_operations_parses_copy_command() -> None:
    skill = FileOperationsSkill()

    source, destination = skill._parse_command(
        "Kopiere test.pdf nach Desktop"
    )

    assert source == "test.pdf"
    assert destination == Path.home() / "Desktop"


def test_file_operations_parses_move_command() -> None:
    skill = FileOperationsSkill()

    source, destination = skill._parse_command(
        "Verschiebe bild.png nach Bilder"
    )

    assert source == "bild.png"
    assert destination == Path.home() / "Pictures"


def test_file_operations_parses_absolute_source_and_destination(
    tmp_path: Path,
) -> None:
    source_path = tmp_path / "Source Files" / "Report.pdf"
    destination_path = tmp_path / "Archive Folder"
    skill = FileOperationsSkill()

    source, destination = skill._parse_command(
        f"Kopiere {source_path} nach {destination_path}"
    )

    assert source == str(source_path)
    assert destination == destination_path
    assert skill.can_handle(f"Kopiere {source_path} nach {destination_path}")


@patch("jarvis.skills.file_operations.FileActions.copy_file", return_value=True)
def test_file_operations_copies_absolute_source_to_absolute_destination(
    copy_file,
    tmp_path: Path,
) -> None:
    source = tmp_path / "Source Files" / "Report.pdf"
    destination_folder = tmp_path / "Archive Folder"
    source.parent.mkdir()
    destination_folder.mkdir()
    source.write_text("report", encoding="utf-8")
    skill = FileOperationsSkill()

    result = skill.execute(f"Kopiere {source} nach {destination_folder}")

    assert result == f"Ich habe 'Report.pdf' nach {destination_folder.name} kopiert."
    copy_file.assert_called_once_with(source, destination_folder / source.name)


@patch("jarvis.skills.file_operations.FileActions.copy_file")
def test_file_operations_does_not_overwrite_existing_destination(
    copy_file,
    tmp_path: Path,
) -> None:
    source = tmp_path / "source.txt"
    destination_folder = tmp_path / "Archive"
    source.write_text("new", encoding="utf-8")
    destination_folder.mkdir()
    (destination_folder / source.name).write_text("existing", encoding="utf-8")
    skill = FileOperationsSkill()

    result = skill.execute(f"Kopiere {source} nach {destination_folder}")

    assert "existiert im Zielordner bereits" in result
    copy_file.assert_not_called()


def test_file_actions_copy_does_not_overwrite_existing_destination(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source.txt"
    destination = tmp_path / "destination.txt"
    source.write_text("new content", encoding="utf-8")
    destination.write_text("keep this", encoding="utf-8")

    assert not FileActions.copy_file(source, destination)
    assert source.read_text(encoding="utf-8") == "new content"
    assert destination.read_text(encoding="utf-8") == "keep this"


def test_file_actions_move_does_not_overwrite_existing_destination(
    tmp_path: Path,
) -> None:
    source = tmp_path / "source.txt"
    destination = tmp_path / "destination.txt"
    source.write_text("new content", encoding="utf-8")
    destination.write_text("keep this", encoding="utf-8")

    assert not FileActions.move_file(source, destination)
    assert source.read_text(encoding="utf-8") == "new content"
    assert destination.read_text(encoding="utf-8") == "keep this"


@patch("jarvis.conversation.manager.FileActions.move_file", return_value=True)
def test_conversation_confirms_move_before_moving_file(
    move_file,
    tmp_path: Path,
) -> None:
    source = tmp_path / "Source Folder" / "Report.pdf"
    destination_folder = tmp_path / "Archive"
    source.parent.mkdir()
    destination_folder.mkdir()
    source.write_text("report", encoding="utf-8")
    manager = ConversationManager(AIRouter())

    response = manager.chat(f"Verschiebe {source} nach {destination_folder}")

    assert "wirklich" in response
    assert "verschieben?" in response
    move_file.assert_not_called()

    result = manager.chat("Ja")

    assert result == "Die Datei wurde verschoben."
    move_file.assert_called_once_with(
        str(source), str(destination_folder / source.name)
    )


@patch("jarvis.conversation.manager.FileActions.move_file")
def test_conversation_can_cancel_move(move_file, tmp_path: Path) -> None:
    source = tmp_path / "Report.pdf"
    destination_folder = tmp_path / "Archive"
    source.write_text("report", encoding="utf-8")
    destination_folder.mkdir()
    manager = ConversationManager(AIRouter())

    manager.chat(f"Verschiebe {source} nach {destination_folder}")
    result = manager.chat("Nein")

    assert result == "Verstanden. Der Vorgang wurde abgebrochen."
    assert manager.pending_action is None
    assert manager.pending_file is None
    assert manager.pending_destination is None
    move_file.assert_not_called()


@patch("jarvis.conversation.manager.FileActions.move_file")
def test_conversation_does_not_overwrite_existing_file_on_move(
    move_file,
    tmp_path: Path,
) -> None:
    source = tmp_path / "Source" / "Report.pdf"
    destination_folder = tmp_path / "Archive"
    source.parent.mkdir()
    destination_folder.mkdir()
    source.write_text("source", encoding="utf-8")
    (destination_folder / source.name).write_text("destination", encoding="utf-8")
    manager = ConversationManager(AIRouter())

    result = manager.chat(f"Verschiebe {source} nach {destination_folder}")

    assert "existiert im Zielordner bereits" in result
    assert manager.pending_action is None
    move_file.assert_not_called()
