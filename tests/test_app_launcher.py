from jarvis.skills.app_launcher import AppLauncherSkill


def test_app_launcher_detects_open():
    skill = AppLauncherSkill()

    assert skill.can_handle("Öffne Chrome")