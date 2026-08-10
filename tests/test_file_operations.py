from pathlib import Path

from jarvis.skills.file_operations import FileOperationsSkill


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