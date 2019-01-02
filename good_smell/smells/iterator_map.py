import ast
from good_smell import AstSmell, LoggingTransformer


class IteratorMap(AstSmell):
    @property
    def symbol(self):
        return "iterator-map"

    @property
    def transformer_class(self):
        return MapTransformer

    @property
    def warning_message(self):
        return "Target is only used with a transformation, this can be moved to the iterator"


class AllNameLoadsSame(ast.NodeVisitor):
    def __init__(self, name: ast.Name):
        self.expr = None
        self.name = name
        self.name.context = ast.Load()


class MapTransformer(LoggingTransformer):
    def is_smelly(self, node: ast.AST):
        return isinstance(node, ast.For)
