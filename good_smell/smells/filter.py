import ast
from typing import cast

from good_smell import AstSmell, LoggingTransformer


class NameReplacer(ast.NodeTransformer):
    def __init__(self, old: ast.Name, new: ast.Name):
        self.old = old
        self.new = new

    def visit_Name(self, node: ast.Name) -> ast.Name:
        if node.id == self.old.id:
            return self.new
        return node


class FilterTransformer(LoggingTransformer):
    """Bumps the filter to the iterator"""

    def visit_For(self, node: ast.For) -> ast.For:
        if_node: ast.If = node.body[0]
        filter_condition: ast.Expr = if_node.test
        iter_generator: ast.GeneratorExp = cast(
            ast.GeneratorExp, ast_node("(x for x in seq)").value
        )
        x_name_node = ast_node("x").value
        iter_comprehension = iter_generator.generators[0]
        name_replacer = NameReplacer(node.target, x_name_node)
        iter_comprehension.iter = name_replacer.visit(node.iter)
        iter_comprehension.ifs.append(name_replacer.visit(filter_condition))
        node.iter = iter_generator
        node.body = if_node.body
        return node

    def is_smelly(self, node: ast.AST):
        """Check if the node is only a nested for"""
        return (
            isinstance(node, ast.For)
            and len(node.body) == 1
            and isinstance(node.body[0], ast.If)
        )


class FilterIterator(AstSmell):
    """Checks for adjacent nested fors and replaces them with itertools.product"""

    @property
    def transformer_class(self):
        return FilterTransformer

    @property
    def warning_message(self):
        return "Consider using itertools.product instead of a nested for"

    @property
    def symbol(self) -> str:
        return "filter-iterator"


def ast_node(expr: str) -> ast.AST:
    """Helper function to parse a string denoting an expression into an AST node"""
    # ast.parse returns "Module(body=[Node])"
    return ast.parse(expr).body[0]
