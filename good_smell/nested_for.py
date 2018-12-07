from good_smell import LintSmell, SmellWarning
import ast
import astor


class NestedFor(LintSmell):
    """Checks for adjacent nested fors and replaces them with itertools.product"""
    WARNING_MESSAGE = "Consider using itertools.product instead of a nested for: https://docs.python.org/3/library/itertools.html#itertools.product"

    def check_for_smell(self) -> SmellWarning:
        """Check if the smell occurs between `starting_line` and `end_line` in `source_code`"""
        transformer = NestedForTransformer()
        transformer.visit(ast.parse(self.source_code))
        node: ast.stmt
        return [SmellWarning(msg=self.WARNING_MESSAGE, row=node.lineno, col=node.col_offset, code=self.code, path=self.path)
                for node in transformer.transformed_nodes]

    def fix_smell(self) -> str:
        """Return a fixed version of the code without the code smell"""
        return astor.to_source(NestedForTransformer().visit(ast.parse(self.source_code)))

    @property
    def code(self):
        return "I01"


class NestedForTransformer(ast.NodeTransformer):
    """NodeTransformer that goes through all the nested `for`s and replaces them with itertools.product"""

    def __init__(self):
        # Tracks all the nodes that were changed from the transformation
        self.transformed_nodes = list()

    def visit_For(self, node: ast.For) -> ast.For:
        if not self.is_nested_for(node):
            return node

        inner_for: ast.For = node.body[0]
        import_itertools = ast_node('import itertools')
        itertools_product = ast_node('itertools.product').value
        new_for = ast.For(
            target=ast.Tuple(elts=[node.target, inner_for.target]),
            iter=ast.Call(func=itertools_product, args=[
                node.iter, inner_for.iter], keywords=[]),
            body=inner_for.body,
            orelse=node.orelse
        )
        new_for = ast.fix_missing_locations(new_for)
        self.transformed_nodes.append(new_for)
        return [ast.copy_location(import_itertools, node), new_for]

    @staticmethod
    def is_nested_for(node: ast.For):
        """Check if the node is only a nested for"""
        try:
            return isinstance(node.body[0], ast.For) and len(node.body) == 1
        except AttributeError:
            return False


def ast_node(expr: str) -> ast.AST:
    """Helper function to parse a string denoting an expression into an AST node"""
    # ast.parse returns "Module(body=[Node])"
    return ast.parse(expr).body[0]
