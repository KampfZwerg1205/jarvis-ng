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