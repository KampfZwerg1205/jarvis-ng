from pathlib import Path

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