"""Evaluate basic arithmetic expressions without executing Python code."""

import ast
import math
import operator


_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}
_MAX_EXPRESSION_LENGTH = 256
_MAX_AST_NODES = 64


def _evaluate_node(node):
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
        return _OPERATORS[type(node.op)](
            _evaluate_node(node.left),
            _evaluate_node(node.right),
        )
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPERATORS:
        return _OPERATORS[type(node.op)](_evaluate_node(node.operand))
    raise ValueError("only numbers and +, -, *, /, and parentheses are allowed")


def evaluate_arithmetic(expression: str):
    """Evaluate a bounded expression containing only basic arithmetic."""
    if not isinstance(expression, str):
        raise TypeError("expression must be a string")
    if len(expression) > _MAX_EXPRESSION_LENGTH:
        raise ValueError("expression is too long")

    tree = ast.parse(expression, mode="eval")
    if sum(1 for _ in ast.walk(tree)) > _MAX_AST_NODES:
        raise ValueError("expression is too complex")

    result = _evaluate_node(tree.body)
    if isinstance(result, float) and not math.isfinite(result):
        raise ValueError("result must be finite")
    return result
