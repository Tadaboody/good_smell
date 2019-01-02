from good_smell import AstSmell, LoggingTransformer


class DropWhile(AstSmell):
    """Checks for a conditional continue in the start of a for
    replaces with usage of itertools.takewhile"""

    @property
    def transformer_class(self):
        return DropWhileTransformer

    @property
    def warning_message(self):
        return "Consider using itertools.product instead of a nested for"

    @property
    def symbol(self) -> str:
        return "filter-iterator"


class DropWhileTransformer(LoggingTransformer):
    def is_smelly(self, node: ast.Node):
        pass
