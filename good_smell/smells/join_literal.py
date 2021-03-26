import ast

from good_smell import AstSmell, LoggingTransformer


class JoinLiteral(AstSmell):
    """Checks if joining a literal of a sequence."""

    @property
    def transformer_class(self):
        return NestedForTransformer

    @property
    def warning_message(self):
        return (
            "Consider using str.format instead of joining a constant amount of strings."
        )

    @property
    def symbol(self):
        return "join-literal"


class NestedForTransformer(LoggingTransformer):
    """NodeTransformer that goes visits all the nested `for`s and replaces them
    with itertools.product"""

    @staticmethod
    def is_smelly(node: ast.AST):
        """Check if the node is only a nested for"""
        return (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Constant)
            and node.func.attr == "join"
            and len(node.args) == 1
            and isinstance(node.args[0], ast.List)
        )
