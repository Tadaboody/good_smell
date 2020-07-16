import ast
from typing import Generator, Tuple

from good_smell import SmellWarning, implemented_smells, __version__


class LintingFlake8:
    """Entry point good smell to be used as a flake8 linting plugin"""

    name = "good-smell"
    version = __version__

    def __init__(self, tree: ast.AST, filename: str):
        """"http://flake8.pycqa.org/en/latest/plugin-development/plugin-parameters.html"""
        self.tree = tree
        self.filename = filename

    def run(self) -> Generator[Tuple[int, int, str, str], None, None]:
        for num, smell in enumerate(implemented_smells):
            warnings = smell(
                transform=False, tree=self.tree, path=self.filename
            ).check_for_smell()
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
