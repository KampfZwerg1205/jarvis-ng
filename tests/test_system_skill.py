from jarvis.skills.system import SystemSkill


def test_system_skill_detects_system_question() -> None:
    skill = SystemSkill()

    assert skill.can_handle("Welches Betriebssystem benutze ich?")


def test_system_skill_returns_system_information() -> None:
    skill = SystemSkill()

    result = skill.execute("Welches Betriebssystem benutze ich?")

    assert "Du verwendest" in result


def test_system_skill_returns_computer_name() -> None:
    skill = SystemSkill()

    result = skill.execute("Wie heißt mein Computer?")

    assert "Der Computer heißt" in result