import ast

from good_smell import AstSmell, LoggingTransformer

try:
    # ast.Str is deprecated in py3.8 and will be removed
    StrConst = (ast.Constant, ast.Str)
except AttributeError:
    StrConst = (ast.Constant,)


class JoinLiteral(AstSmell):
    """Checks if joining a literal of a sequence."""

    @property
    def transformer_class(self):
        return Transformer

    @property
    def warning_message(self):
        return (
            "Consider using str.format instead of joining a constant amount of strings."
        )

    @property
    def symbol(self):
        return "join-literal"


class Transformer(LoggingTransformer):
    """Checks for usages of str.join with a constant amount of arguments."""

    @staticmethod
    def normalize_constant(node) -> ast.Constant:
        """Compatibility wrapper for py3.8+, ast, ast.Str and ast.Num are replaced by ast.Constant.

        We don't type annotate `node` so it doesn't break on py3.10+ when these classes will be removed.
        """
        for attr in ["value", "s", "n"]:
            try:
                return ast.Constant(value=getattr(node, attr))
            except AttributeError:
                pass
        raise ValueError("Not a constat.")

    def visit_Call(self, node: ast.Call) -> ast.Call:
        format_arguments = node.args[0].elts
        format_delimiter = self.normalize_constant(node.func.value).value
        format_string = format_delimiter.join(["{}"] * len(format_arguments))
        new_call = ast.Call(
            func=ast.Attribute(
                value=ast.Constant(value=format_string), attr="format", ctx=ast.Load()
            ),
            args=format_arguments,
            keywords=[],
        )
        return ast.fix_missing_locations(new_call)

    @staticmethod
    def is_smelly(node: ast.AST):
        """Check if the node is only a nested for"""
        return (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, StrConst)
            and node.func.attr == "join"
            and len(node.args) == 1
            and isinstance(node.args[0], ast.List)
            and not any(isinstance(el, ast.Starred) for el in node.args[0].elts)
        )
