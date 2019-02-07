import ast
from good_smell import AstSmell, LoggingTransformer
from typing import List


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


class ASTComperator:
    def __init__(self):
        self.compared_dict = dict()

    @staticmethod
    def cmp_values(node: ast.AST):
        yield from (
            value
            for field, value in ast.iter_fields(node)
            if field not in ["lineno", "colno"]
        )

    def compare(self, a: ast.AST, b: ast.AST):
        same_instance = isinstance(a, type(b))
        same_fields = all(
            self.compare_fields(val_a, val_b)
            for (val_a, val_b) in zip(self.cmp_values(a), self.cmp_values(b))
        )
        comparison = same_instance and same_fields
        self.compared_dict[(a, b)] = comparison
        return comparison

    def compare_fields(self, a, b):
        if not isinstance(a, type(b)):
            return False
        if isinstance(a, ast.AST):
            try:
                return self.compared_dict[(a, b)]
            except KeyError:
                return self.compare(a, b)
        if isinstance(a, list):
            return all(self.compare_fields(a_elm, b_elm) for a_elm, b_elm in zip(a, b))
        return a == b


class AllNameLoadsSame(ast.NodeVisitor):
    def __init__(self, name: ast.Name, root):
        self.expr = None
        self.name = name
        self.__name_loads: List[ast.Name] = list()
        self.comperator = ASTComperator()

    def visit(self, node: ast.AST):
        """Overrite visit to add a parent attribute"""
        assert isinstance(node, ast.AST), "Not an AST!"
        for _, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in (i for i in value if isinstance(i, ast.AST)):
                    item.parent = node
            if isinstance(value, ast.AST):
                value.parent = node
        super().visit(node)

    def visit_Name(self, node: ast.Name):
        if (
            isinstance(node, ast.Name)
            and node.id == self.name.id
            and isinstance(node.ctx, ast.Load)
        ):
            self.__name_loads.append(node)
        return self.generic_visit(node)

    def biggest_common_expression(self):
        highest_node = self.__name_loads[0]
        current = self.__name_loads
        while all(current[0] == val for val in current):
            highest_node = current[0]
            current = [val.parent for val in current]
        return highest_node


class MapTransformer(LoggingTransformer):
    def is_smelly(self, node: ast.AST):
        if isinstance(node, ast.For):
            self.ally = AllNameLoadsSame(node.target)
            self.ally.visit(node)
            return not isinstance(self.ally.biggest_common_expression(), ast.Name)
