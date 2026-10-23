from pathlib import Path
from unittest.mock import patch

from jarvis.skills.file_manager import FileManagerSkill
from jarvis.skills.registry import SkillRegistry
from jarvis.skills.router import SkillRouter


def test_file_manager_detects_subfolder_command() -> None:
    skill = FileManagerSkill()
    assert skill.can_handle("Öffne den Ordner kram auf dem Desktop")
    assert skill.can_handle("Öffne den Ordner kram")


def test_file_manager_opens_subfolder_on_desktop(tmp_path: Path) -> None:
    desktop = tmp_path / "Desktop"
    folder = desktop / "kram"
    folder.mkdir(parents=True)
    skill = FileManagerSkill()

    with (
        patch("jarvis.skills.file_manager.Path.home", return_value=tmp_path),
        patch("jarvis.skills.file_manager.FileActions.open_path", return_value=True) as open_path,
    ):
        result = skill.execute("Öffne den Ordner kram auf dem Desktop")

    assert result == "Ich öffne den Ordner 'kram'."
    open_path.assert_called_once_with(folder)


def test_file_manager_does_not_open_path_traversal(tmp_path: Path) -> None:
    skill = FileManagerSkill()

    with (
        patch("jarvis.skills.file_manager.Path.home", return_value=tmp_path),
        patch("jarvis.skills.file_manager.FileActions.open_path") as open_path,
    ):
        assert not skill.can_handle(
            "\u00d6ffne den Ordner ..\\Documents auf dem Desktop"
        )
        open_path.assert_not_called()


def test_file_manager_opens_folder_found_anywhere(tmp_path: Path) -> None:
    folder = tmp_path / "Projects" / "kram"
    folder.mkdir(parents=True)
    skill = FileManagerSkill()

    with (
        patch.object(skill, "_find_matching_folders", return_value=[folder]),
        patch("jarvis.skills.file_manager.FileActions.open_path", return_value=True) as open_path,
    ):
        result = skill.execute("Öffne den Ordner kram")

    assert result == "Ich öffne den Ordner 'kram'."
    open_path.assert_called_once_with(folder)


def test_file_manager_opens_folder_by_absolute_path(tmp_path: Path) -> None:
    folder = tmp_path / "My Folder"
    folder.mkdir()
    skill = FileManagerSkill()

    with patch(
        "jarvis.skills.file_manager.FileActions.open_path",
        return_value=True,
    ) as open_path:
        result = skill.execute(f"Öffne den Ordner {folder}")

    assert skill.can_handle(f"Öffne den Ordner {folder}")
    assert result == "Ich öffne den Ordner 'My Folder'."
    open_path.assert_called_once_with(folder)


def test_file_manager_asks_for_location_when_folder_name_is_ambiguous(
    tmp_path: Path,
) -> None:
    first = tmp_path / "Projects" / "kram"
    second = tmp_path / "Documents" / "kram"
    skill = FileManagerSkill()

    with (
        patch.object(skill, "_find_matching_folders", return_value=[first, second]),
        patch("jarvis.skills.file_manager.FileActions.open_path") as open_path,
    ):
        result = skill.execute("Öffne den Ordner kram")

    assert "mehrere Ordner namens 'kram'" in result
    assert str(first) in result
    assert str(second) in result
    open_path.assert_not_called()


def test_router_selects_file_manager_for_subfolder_command() -> None:
    registry = SkillRegistry()
    registry.load_defaults()
    router = SkillRouter()
    for skill in registry.all():
        router.register(skill)

    selected = router.find("Öffne den Ordner kram auf dem Desktop")

    assert selected is not None
    assert selected.name == "file_manager"
