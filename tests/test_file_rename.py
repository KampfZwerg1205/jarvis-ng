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