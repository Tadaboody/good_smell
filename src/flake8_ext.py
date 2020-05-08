import ast
import math
from good_smell import implemented_smells, SmellWarning
from typing import Tuple, Generator


class GoodSmellFlake8:
    """Entry point good smell to be used as a flake8 plugin"""

    name = "good-smell"
    version = "0.1"

    def __init__(self, tree: ast.AST, filename: str):
        """"http://flake8.pycqa.org/en/latest/plugin-development/plugin-parameters.html"""
        self.tree = tree
        self.filename = filename

    def run(self) -> Generator[Tuple[int, int, str, str], None, None]:
        for num, smell in enumerate(implemented_smells):
            warnings = smell(tree=self.tree, path=self.filename).check_for_smell()
            warning: SmellWarning
            yield from (
                (
                    warning.row,
                    warning.col,
                    f"SML{str(num).zfill(3)} {warning.msg}",
                    "GoodSmell",
                )
                for warning in warnings
            )
