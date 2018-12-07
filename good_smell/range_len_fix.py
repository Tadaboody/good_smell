import ast
import logging
from ast import *
from typing import Union

import astor
from astpretty import pformat, pprint

from good_smell import LintSmell, SmellWarning


class RangeLenSmell(LintSmell):
    WARNING_MESSAGE = "Instead of using a c-style for loop, try using enumerate!"
    def check_for_smell(self) -> SmellWarning:
        """Check if the smell occurs between `starting_line` and `end_line` in `source_code`"""
        transformer = EnumerateFixer()
        transformer.visit(ast.parse(self.source_code))
        node: ast.stmt
        return [SmellWarning(msg=self.WARNING_MESSAGE, row=node.lineno, col=node.col_offset, code=self.code, path=self.path)
                for node in transformer.transformed_nodes]

    def fix_smell(self) -> str:
        """Return a fixed version of the code without the code smell"""
        return astor.to_source(EnumerateFixer().visit(ast.parse(self.source_code)))

    @property
    def code(self):
        return "W01"


class AssignDeleter(NodeTransformer):
    def __init__(self, seq: ast.Name, target: ast.Name):
        self.id = target
        self.seq = seq
        self.elem_target = None

    def visit_Assign(self, node: ast.Assign):
        """Deletes a node if it assigning using the for target"""
        if isinstance(node.value, ast.Subscript) and node.value.slice.value.id == self.id.id and node.value.value.id == self.seq.id:
            self.elem_target = node.targets[0]
            return None
        return node


class EnumerateFixer(NodeTransformer):
    def __init__(self):
        self.transformed_nodes = list()

    def visit_For(self, node: ast.For) -> Union[bool, ast.For]:
        logging.debug("visit")
        if not self.is_range_len(node):
            return node

        logging.debug("found")
        enumerate_node = Name(id='enumerate', ctx=Load())
        node_iterable = node.iter.args[0].args[0]
        original_target = node.target
        deleter = AssignDeleter(target=original_target, seq=node_iterable)
        new_body = deleter.visit(node).body or [Pass()]
        elm_target = deleter.elem_target or Name(id='elm', ctx=Store())
        # for (original_target,elm_target) in enumerate(node_iterable):
        new_node = For(target=Tuple(elts=[original_target, elm_target], ctx=Store()),
                       iter=Call(
            func=enumerate_node, args=[node_iterable], keywords=[]),
            body=new_body,
            orelse=node.orelse)
        new_node = ast.fix_missing_locations(copy_location(new_node, node))
        self.transformed_nodes.append(new_node)
        return new_node

    @staticmethod
    def is_range_len(node: ast.For):
        try:
            logging.debug("check")
            logging.debug(pformat(node))
            return node.iter.func.id == 'range' and node.iter.args[0].func.id == 'len'
        except AttributeError as e:
            logging.debug("attr error!" + str(e))
            return False
