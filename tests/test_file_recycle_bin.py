from unittest.mock import patch

from jarvis.skills.file_recycle_bin import FileRecycleBinSkill


def test_file_recycle_bin_name() -> None:
    skill = FileRecycleBinSkill()

    assert skill.name == "file_recycle_bin"


def test_file_recycle_bin_can_handle_open() -> None:
    skill = FileRecycleBinSkill()

    assert skill.can_handle("Öffne den Papierkorb")


def test_file_recycle_bin_can_handle_show() -> None:
    skill = FileRecycleBinSkill()

    assert skill.can_handle("Zeige mir den Papierkorb")


def test_file_recycle_bin_rejects_unrelated_prompt() -> None:
    skill = FileRecycleBinSkill()

    assert not skill.can_handle("Öffne den Desktop")


def test_file_recycle_bin_confidence() -> None:
    skill = FileRecycleBinSkill()

    assert skill.confidence("Öffne den Papierkorb") == 1.0
    assert skill.confidence("Öffne den Desktop") == 0.0


@patch(
    "jarvis.skills.file_recycle_bin.FileActions.open_recycle_bin",
    return_value=True,
)
def test_file_recycle_bin_execute_success(mock_open) -> None:
    skill = FileRecycleBinSkill()

    result = skill.execute("Öffne den Papierkorb")

    assert result == "Der Papierkorb wurde geöffnet."
    mock_open.assert_called_once()


@patch(
    "jarvis.skills.file_recycle_bin.FileActions.open_recycle_bin",
    return_value=False,
)
def test_file_recycle_bin_execute_failure(mock_open) -> None:
    skill = FileRecycleBinSkill()

    result = skill.execute("Öffne den Papierkorb")

    assert result == "Der Papierkorb konnte nicht geöffnet werden."
    mock_open.assert_called_once()