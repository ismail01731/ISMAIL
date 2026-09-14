from __future__ import annotations
import ast
import operator
from dataclasses import dataclass
@dataclass(frozen=True)
class CalculationResult:
    success: bool
    expression: str
    result: int | float | None = None
    reason: str = ""
class SafeCalculator:
    """
    Deterministic arithmetic calculator.
    Safety:
    - Uses Python AST parsing.
    - Never uses eval() or exec().
    - Allows only numeric literals and approved arithmetic operators.
    - Does not execute arbitrary Python code.
    """
    _BINARY_OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.FloorDiv: operator.floordiv,
    }
    _UNARY_OPERATORS = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }
    def calculate(self, expression: str) -> CalculationResult:
        if not isinstance(expression, str) or not expression.strip():
            return CalculationResult(
                success=False,
                expression=str(expression),
                reason="Calculation expression cannot be empty.",
            )
        expression = expression.strip()
        try:
            tree = ast.parse(expression, mode="eval")
        except (SyntaxError, ValueError):
            return CalculationResult(
                success=False,
                expression=expression,
                reason="Invalid arithmetic expression.",
            )
        try:
            result = self._evaluate(tree.body)
        except ZeroDivisionError:
            return CalculationResult(
                success=False,
                expression=expression,
                reason="Division by zero is not allowed.",
            )
        except (OverflowError, ValueError):
            return CalculationResult(
                success=False,
                expression=expression,
                reason="Calculation value is outside the supported range.",
            )
        except (TypeError, ArithmeticError):
            return CalculationResult(
                success=False,
                expression=expression,
                reason="Unsupported arithmetic operation.",
            )
        if not isinstance(result, (int, float)) or isinstance(result, bool):
            return CalculationResult(
                success=False,
                expression=expression,
                reason="Only numeric results are supported.",
            )
        return CalculationResult(
            success=True,
            expression=expression,
            result=result,
            reason="Calculation completed successfully.",
        )
    def _evaluate(self, node: ast.AST) -> int | float:
        if isinstance(node, ast.Constant):
            value = node.value
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise TypeError
            return value
        if isinstance(node, ast.BinOp):
            operation = self._BINARY_OPERATORS.get(type(node.op))
            if operation is None:
                raise TypeError
            left = self._evaluate(node.left)
            right = self._evaluate(node.right)
            if isinstance(node.op, ast.Pow):
                if abs(right) > 1000:
                    raise ValueError
            return operation(left, right)
        if isinstance(node, ast.UnaryOp):
            operation = self._UNARY_OPERATORS.get(type(node.op))
            if operation is None:
                raise TypeError
            return operation(self._evaluate(node.operand))
        raise TypeError
calculator = SafeCalculator()
