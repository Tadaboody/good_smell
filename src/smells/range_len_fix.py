import ast

from good_smell import AstSmell, LoggingTransformer
from typing import Union


class RangeLenSmell(AstSmell):
    @property
    def transformer_class(self):
        return EnumerateFixer

    @property
    def symbol(self):
        return "range-len"

    @property
    def warning_message(self) -> str:
        return "Instead of using a c-style for loop, try using enumerate!"


class AssignDeleter(ast.NodeTransformer):
    def __init__(self, seq: ast.Name, target: ast.Name):
        self.id = target
        self.seq = seq
        self.elem_target = None or ast.Name(id="elm", ctx=ast.Store())
        self.uses_seq = False

    def visit_Assign(self, node: ast.Assign):
        """Deletes a node if it assigning using the for target"""
        if self.accesses_seq(node.value):
            self.elem_target = node.targets[0]
            return None
        return self.generic_visit(node)

    def accesses_seq(self, node) -> bool:
        """Checks if the node acceses the sequence[target]"""
        if (
            isinstance(node, ast.Subscript)
            and node.slice.value.id == self.id.id
            and node.value.id == self.seq.id
        ):
            self.uses_seq = True
            return True

    def visit_Subscript(self, node: ast.Subscript):
        if self.accesses_seq(node):
            return self.elem_target
        return self.generic_visit(node)


class EnumerateFixer(LoggingTransformer):
    def visit_For(self, node: ast.For) -> Union[bool, ast.For]:
        enumerate_node = ast.Name(id="enumerate", ctx=ast.Load())
        node_iterable = node.iter.args[0].args[0]
        original_target = node.target
        deleter = AssignDeleter(target=original_target, seq=node_iterable)
        new_body = deleter.visit(node).body or [ast.Pass()]
        elm_target = (
            deleter.elem_target
            if deleter.uses_seq
            else ast.Name(id="_", ctx=ast.Store())
        )
        # for (original_target,elm_target) in enumerate(node_iterable):
        new_node = ast.For(
            target=ast.Tuple(elts=[original_target, elm_target], ctx=ast.Store()),
            iter=ast.Call(func=enumerate_node, args=[node_iterable], keywords=[]),
            body=new_body,
            orelse=node.orelse,
        )
        new_node = ast.fix_missing_locations(ast.copy_location(new_node, node))
        new_node = self.generic_visit(new_node)
        return new_node

    @staticmethod
    def is_smelly(node: ast.For):
        try:
            return node.iter.func.id == "range" and node.iter.args[0].func.id == "len"
        except AttributeError:
            return False
