from iter_lint import LintSmell
import ast
from typing import Union
import astor


class NestedFor(LintSmell):
    """Checks for adjacent nested fors and replaces them with itertools.product"""

    def check_for_smell(self) -> bool:
        """Check if the smell occurs between `starting_line` and `end_line` in `source_code`"""
        return NestedForTransformer(change_node=False).visit(ast.parse(self.source_code))

    def fix_smell(self) -> str:
        """Return a fixed version of the code without the code smell"""
        return astor.to_source(NestedForTransformer(change_node=True).visit(ast.parse(self.source_code)))


class NestedForTransformer(ast.NodeTransformer):
    def __init__(self, change_node: bool):
        self.change_node = change_node

    def visit_For(self, node: ast.For) -> Union[bool, ast.For]:
        if not self.change_node and self.is_nested_for(node):
            return True

        if self.is_nested_for(node):
            inner_for = node.body[0]
            inner_target = inner_for.target
            import_itertools = ast_node('import itertools')
            itertools_product = ast_node('itertools.product').value
            new_for = ast.For(
                target=ast.Tuple(elts=[node.target, inner_for.target]),
                iter=ast.Call(func=itertools_product, args=[
                              node.iter, inner_for.iter], keywords=[]),
                body=inner_for.body + node.body[1:],
                orelse=node.orelse
            )
            return [ast.copy_location(import_itertools, node), ast.fix_missing_locations(new_for)]
        return node

    @staticmethod
    def is_nested_for(node: ast.For):
        try:
            return isinstance(node.body[0], ast.For)
        except AttributeError as e:
            return False


def ast_node(expr: str) -> ast.AST:
    """Helper function to parse a string denoting an expression into an AST node"""
    # ast.parse returns "Module(body=[Node])"
    return ast.parse(expr).body[0]
