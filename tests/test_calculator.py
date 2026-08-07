from jarvis.skills.calculator import CalculatorSkill


def test_calculator_skill() -> None:
    skill = CalculatorSkill()

    assert skill.can_handle("Was ist 25 * 4?")
    assert skill.execute("Was ist 25 * 4?") == "Das Ergebnis ist 100."