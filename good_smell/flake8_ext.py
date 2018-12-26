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
                    f"SML{self.leading_digit_str(num,3)} {warning.msg}",
                    "GoodSmell",
                )
                for warning in warnings
            )

    @staticmethod
    def leading_digit_str(num: int, digits: int) -> str:
        """Adds leading 0's to num to make him `digits` long"""
        missing_0s = digits - int(math.log10(num)) - 1
        return f"{'0'*missing_0s}{num}"
