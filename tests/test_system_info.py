from jarvis.skills.system_info import SystemInfoSkill


def test_system_info_does_not_match_ram_inside_another_word() -> None:
    assert not SystemInfoSkill().can_handle(
        "Öffne den Ordner kram auf dem Desktop"
    )


def test_system_info_still_detects_ram_questions() -> None:
    skill = SystemInfoSkill()
    assert skill.can_handle("Wie viel RAM habe ich?")
    assert skill.can_handle("RAM")
