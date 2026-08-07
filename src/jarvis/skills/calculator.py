from __future__ import annotations

import ast
import operator

from jarvis.skills.base import Skill


class CalculatorSkill(Skill):
    """Führt sichere mathematische Berechnungen aus."""

    _operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
    }

    @property
    def name(self) -> str:
        return "calculator"

    def can_handle(self, prompt: str) -> bool:
        prompt = prompt.lower().strip()

        math_keywords = (
            "rechne",
            "berechne",
            "was ist",
            "wie viel ist",
        )

        return (
            any(keyword in prompt for keyword in math_keywords)
            and any(char.isdigit() for char in prompt)
        )

    def confidence(self, prompt: str) -> float:
        if self.can_handle(prompt):
            return 0.9

        return 0.0

    def execute(self, prompt: str) -> str:
        expression = self._extract_expression(prompt)

        try:
            tree = ast.parse(expression, mode="eval")
            result = self._evaluate(tree.body)
        except (SyntaxError, ValueError, ZeroDivisionError):
            return "Ich konnte diese Berechnung nicht ausführen."

        return f"Das Ergebnis ist {result}."

    def _extract_expression(self, prompt: str) -> str:
        expression = prompt.lower()

        for phrase in (
            "rechne",
            "berechne",
            "was ist",
            "wie viel ist",
        ):
            expression = expression.replace(phrase, "")

        return expression.strip().replace(",", ".").rstrip("?!.,")

    def _evaluate(self, node: ast.AST) -> float | int:
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value

            raise ValueError("Ungültiger Wert.")

        if isinstance(node, ast.BinOp):
            operation = self._operators.get(type(node.op))

            if operation is None:
                raise ValueError("Operator nicht erlaubt.")

            left = self._evaluate(node.left)
            right = self._evaluate(node.right)

            return operation(left, right)

        if isinstance(node, ast.UnaryOp):
            operation = self._operators.get(type(node.op))

            if operation is None:
                raise ValueError("Operator nicht erlaubt.")

            operand = self._evaluate(node.operand)

            return operation(operand)

        raise ValueError("Ungültiger mathematischer Ausdruck.")