from good_smell import AstSmell, LoggingTransformer
import ast


class NestedFor(AstSmell):
    """Checks for adjacent nested fors and replaces them with itertools.product"""

    @property
    def transformer_class(self):
        return NestedForTransformer

    @property
    def warning_message(self):
        return "Consider using itertools.product instead of a nested for"

    @property
    def code(self):
        return "SML002"

    @property
    def symbol(self):
        return "nested-for"


class NestedForTransformer(LoggingTransformer):
    """NodeTransformer that goes visits all the nested `for`s and replaces them
    with itertools.product"""

    def visit_For(self, node: ast.For) -> ast.For:
        inner_for: ast.For = node.body[0]
        import_itertools = ast_node("import itertools")
        itertools_product = ast_node("itertools.product").value
        new_for = ast.For(
            target=ast.Tuple(elts=[node.target, inner_for.target]),
            iter=ast.Call(
                func=itertools_product, args=[node.iter, inner_for.iter], keywords=[]
            ),
            body=inner_for.body,
            orelse=node.orelse,
        )
        new_for = ast.fix_missing_locations(new_for)
        return [ast.copy_location(import_itertools, node), new_for]

    @staticmethod
    def is_smelly(node: ast.AST):
        """Check if the node is only a nested for"""
        try:
            return (
                isinstance(node, ast.For)
                and isinstance(node.body[0], ast.For)
                and len(node.body) == 1
            )
        except AttributeError:
            return False


def ast_node(expr: str) -> ast.AST:
    """Helper function to parse a string denoting an expression into an AST node"""
    # ast.parse returns "Module(body=[Node])"
    return ast.parse(expr).body[0]
