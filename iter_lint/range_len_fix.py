import ast
import logging
from ast import *
from typing import Union

import astor
from astpretty import pformat, pprint

from iter_lint import LintSmell


class RangeLenSmell(LintSmell):
    class EnumerateFixer(NodeTransformer):
        def __init__(self, change_node: bool):
            self.change_node = change_node

        def visit_For(self, node: ast.For) -> Union[bool, ast.For]:
            logging.debug("visit")
            if not self.change_node and self.is_range_len(node): # TODO: 
                return True

            if self.is_range_len(node):
                logging.debug("found")
                enumerate_node = Name(id='enumerate', ctx=Load())
                node: For
                node_iterable = node.iter.args[0].args[0]
                return ast.fix_missing_locations(copy_location(For(target=Tuple(elts=[Name(id='i', ctx=Store()), Name(id='elm', ctx=Store())], ctx=Store()),
                                                                   iter=Call(
                    func=enumerate_node, args=[node_iterable], keywords=[]),
                    body=node.body,
                    orelse=node.orelse), node))
            return node

        @staticmethod
        def is_range_len(node: ast.For):
            try:
                logging.debug("check")
                logging.debug(pformat(node))
                return node.iter.func.id == 'range' and node.iter.args[0].func.id == 'len'
            except AttributeError as e:
                logging.debug("attr error!" + str(e))
                return False

    def check_for_smell(self) -> bool:
        """Check if the smell occurs between `starting_line` and `end_line` in `source_code`"""
        return self.EnumerateFixer(change_node=False).visit(ast.parse(self.source_code))

    def fix_smell(self) -> str:
        """Return a fixed version of the code without the code smell"""
        return astor.to_source(self.EnumerateFixer(change_node=True).visit(ast.parse(self.source_code)))


def swap_enumerate(code: str):
    return EnumerateFixer().visit(ast.parse(code))
