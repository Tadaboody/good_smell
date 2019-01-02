import ast
from good_smell import AstSmell, LoggingTransformer


class DropWhile(AstSmell):
    """Checks for a conditional continue in the start of a for
    replaces with usage of itertools.takewhile"""

    @property
    def transformer_class(self):
        return DropWhileTransformer

    @property
    def warning_message(self):
        return "Move iteration logic to for using itertools.takewhile"

    @property
    def symbol(self) -> str:
        return "missing-dropwhile"


class DropWhileTransformer(LoggingTransformer):
    def is_smelly(self, node: ast.AST) -> bool:
        if isinstance(node, ast.For) and isinstance(node.body[0], ast.If):
            print("a")
            if_node = node.body[0]
            return len(if_node.body) == 1 and isinstance(if_node.body[0], ast.Continue)

    def visit_For(self, node: ast.For):
        continue_test = node.body[0].test
        dropwhile_predicate = None
        if isinstance(continue_test, ast.Call):
            dropwhile_predicate = continue_test.func
        else:
            dropwhile_predicate = ast.Lambda(
                args=ast.arguments(
                    args=[ast.arg(arg=node.target.id, annotation=None)],
                    vararg=None,
                    kwonlyargs=[],
                    kw_defaults=[],
                    kwarg=None,
                    defaults=[],
                ),
                body=continue_test,
            )
        import_itertools = ast.parse("import itertools").body[0]
        ast.copy_location(node, import_itertools)
        dropwhile = ast.parse("itertools.dropwhile()").body[0].value
        dropwhile.args = [dropwhile_predicate, node.iter]
        new_node = ast.For(
            target=node.target, iter=dropwhile, body=node.body[1:], orelse=node.orelse
        )
        new_node = ast.fix_missing_locations(new_node)
        node.iter = dropwhile
        return [import_itertools, new_node]


"""
Expr(
    lineno=1,
    col_offset=0,
    value=Lambda(
        lineno=1,
        col_offset=0,
        args=arguments(
            args=[arg(lineno=1, col_offset=7, arg='p', annotation=None)],
            vararg=None,
            kwonlyargs=[],
            kw_defaults=[],
        kwarg=None,
            defaults=[],
        ),
        body=Call(
            lineno=1,
            col_offset=9,
            func=Name(lineno=1, col_offset=9, id='print', ctx=Load()),
            args=[Name(lineno=1, col_offset=15, id='p', ctx=Load())],
            keywords=[],
        ),
    ),
)
"""
