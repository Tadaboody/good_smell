from typing import TypeVar
import ast
from typing import cast

from good_smell import AstSmell, LoggingTransformer


class NameReplacer(ast.NodeTransformer):
    def __init__(self, old: ast.Name, new: ast.AST):
        self.old = old
        self.new = new

    def visit_Name(self, node: ast.Name) -> ast.AST:
        if node.id == self.old.id:
            return self.new
        return node


T = TypeVar('T', bound=ast.AST)


def replace_name_with_node(node: T, old_val: ast.Name, new_val: ast.AST) -> T:
    """Returns `node` with all occurences of `old_val` (a variable) replaced with `new_val` (an expression)"""
    return NameReplacer(old_val, new_val).visit(node)


class FilterTransformer(LoggingTransformer):
    """Bumps the filter to the iterator"""

    def visit_For(self, node: ast.For) -> ast.For:
        if_node: ast.If = node.body[0]
        filter_condition: ast.Expr = if_node.test
        if not isinstance(node.iter, ast.GeneratorExp):
            # Create a generator expression if it doesn't exist
            GEN_ELT_NAME = 'x'
            gen_exp: ast.GeneratorExp = cast(
                ast.GeneratorExp, ast_node(f"({GEN_ELT_NAME} for {GEN_ELT_NAME} in seq)").value
            )
            gen_target = ast_node(GEN_ELT_NAME).value
            iter_comprehension = gen_exp.generators[0]
            iter_comprehension.iter = replace_name_with_node(
                node.iter, node.target, gen_target)
        else:
            gen_exp = node.iter
            iter_comprehension = gen_exp.generators[0]
            gen_target = gen_exp.elt

        iter_comprehension.ifs.append(replace_name_with_node(
            filter_condition, node.target, gen_target))
        node.iter = gen_exp
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
