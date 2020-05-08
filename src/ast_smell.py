import ast
import astor
from good_smell import SmellWarning, LintSmell
from typing import Type, List
import abc


class LoggingTransformer(ast.NodeTransformer, abc.ABC):
    """A subclass of transformer that logs the nodes it transforms"""

    def __init__(self):
        self.transformed_nodes = list()

    @abc.abstractmethod
    def is_smelly(self, node: ast.AST) -> bool:
        """Checks if the given `node` should be transformed"""

    def visit(self, node: ast.AST):
        if not self.is_smelly(node):
            return self.generic_visit(node)
        self.transformed_nodes.append(node)
        return super().visit(node)


class AstSmell(LintSmell):
    def check_for_smell(self) -> List[SmellWarning]:
        """Return a list of all occuring smells of this smell class"""
        transformer = self.transformer_class()
        transformer.visit(self.tree)
        node: ast.stmt
        return [
            SmellWarning(
                msg=self.warning_message,
                row=node.lineno,
                col=node.col_offset,
                path=self.path,
                symbol=self.symbol
            )
            for node in transformer.transformed_nodes
        ]

    def fix_smell(self) -> str:
        """Return a fixed version of the code without the code smell"""
        return astor.to_source(self.transformer_class().visit(self.tree))

    @property
    @abc.abstractmethod
    def transformer_class(self) -> Type[LoggingTransformer]:
        """The class for the transformer used to create"""
