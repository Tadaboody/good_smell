from good_smell import AstSmell, LoggingTransformer
import ast


class YieldFrom(AstSmell):
    """Checks for yields inside for loops"""

    @property
    def transformer_class(self):
        return YieldFromTransformer

    @property
    def warning_message(self):
        return "Consider using yield from instead of yield inside of a for loop"

    @property
    def symbol(self):
        return "yield-from"


class YieldFromTransformer(LoggingTransformer):
    """NodeTransformer that goes visits all the yields in fors and replaces them
    with yield from"""

    def visit_For(self, node: ast.For):
        yield_from = ast.Expr(value=ast.YieldFrom(node.iter))
        return ast.fix_missing_locations(yield_from)

    @staticmethod
    def is_smelly(node: ast.AST):
        """Check if the node is a yield inside a for"""
        return (
            isinstance(node, ast.For)
            and len(node.body) == 1
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Yield)
        )
