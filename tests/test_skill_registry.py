from jarvis.skills.registry import SkillRegistry


def test_default_skills_are_loaded() -> None:
    registry = SkillRegistry()

    registry.load_defaults()

    skills = registry.all()
    names = {skill.name for skill in skills}

    assert "time" in names
    assert "calculator" in names