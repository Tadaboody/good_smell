import ast
import astor
from good_smell import SmellWarning, LintSmell
from typing import Type, List
import abc


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

    @abc.abstractmethod
    def transformer_class(self) -> Type[ast.NodeTransformer]:
        """The class for the transformer used to create"""
