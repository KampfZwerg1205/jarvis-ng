from unittest.mock import patch

from jarvis.skills.system_actions import SystemActionSkill


def test_system_action_skill_detects_notepad() -> None:
    skill = SystemActionSkill()

    assert skill.can_handle("Öffne Notepad")


def test_system_action_skill_detects_calculator() -> None:
    skill = SystemActionSkill()

    assert skill.can_handle("Öffne den Taschenrechner")


@patch("jarvis.skills.system_actions.SystemActions.open_notepad")
def test_system_action_skill_opens_notepad(mock_open) -> None:
    skill = SystemActionSkill()

    result = skill.execute("Öffne Notepad")

    mock_open.assert_called_once()
    assert result == "Notepad wurde geöffnet."