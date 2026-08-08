from unittest.mock import patch

from jarvis.skills.volume import VolumeSkill


def test_volume_skill_handles_louder() -> None:
    skill = VolumeSkill()

    assert skill.can_handle("Mach lauter") is True
    assert skill.confidence("Mach lauter") == 1.0


@patch("jarvis.skills.volume.SystemActions.volume_up")
def test_volume_skill_increases_volume(mock_volume_up) -> None:
    mock_volume_up.return_value = True

    skill = VolumeSkill()

    result = skill.execute("Mach lauter")

    mock_volume_up.assert_called_once()
    assert result == "Die Lautstärke wurde erhöht."


@patch("jarvis.skills.volume.SystemActions.volume_down")
def test_volume_skill_decreases_volume(mock_volume_down) -> None:
    mock_volume_down.return_value = True

    skill = VolumeSkill()

    result = skill.execute("Mach leiser")

    mock_volume_down.assert_called_once()
    assert result == "Die Lautstärke wurde verringert."


@patch("jarvis.skills.volume.SystemActions.volume_mute")
def test_volume_skill_mutes_volume(mock_volume_mute) -> None:
    mock_volume_mute.return_value = True

    skill = VolumeSkill()

    result = skill.execute("Stumm schalten")

    mock_volume_mute.assert_called_once()
    assert result == "Der Ton wurde umgeschaltet."


def test_volume_skill_does_not_handle_unrelated_prompt() -> None:
    skill = VolumeSkill()

    assert skill.can_handle("Öffne Discord") is False
    assert skill.confidence("Öffne Discord") == 0.0