from jarvis.skills.router import SkillRouter
from jarvis.skills.time import TimeSkill
from jarvis.skills.calculator import CalculatorSkill


def test_skill_router_finds_time_skill() -> None:
    router = SkillRouter()
    router.register(TimeSkill())
    router.register(CalculatorSkill())

    skill = router.find("Wie spät ist es?")

    assert skill is not None
    assert skill.name == "time"


def test_skill_router_finds_calculator_skill() -> None:
    router = SkillRouter()
    router.register(TimeSkill())
    router.register(CalculatorSkill())

    skill = router.find("Was ist 25 * 4?")

    assert skill is not None
    assert skill.name == "calculator"


def test_skill_router_returns_none_for_unknown_prompt() -> None:
    router = SkillRouter()
    router.register(TimeSkill())
    router.register(CalculatorSkill())

    skill = router.find("Erkläre mir schwarze Löcher.")

    assert skill is None