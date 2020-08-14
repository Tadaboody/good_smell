import ast
from typing import Generator, Tuple
import warnings as python_warnings

from good_smell import SmellWarning, implemented_smells, __version__


def get_traceback():
    import traceback
    import sys
    import os

    _, _, tb = sys.exc_info()
    return os.linesep.join(traceback.format_tb(tb))


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
            try:
                warnings = smell(
                    transform=False, tree=self.tree, path=self.filename
                ).check_for_smell()
            except Exception:
                ISSUE_LINK = "https://github.com/Tadaboody/good_smell/issues/new?assignees=&labels=bug%2C+new&template=bug_report.md"
                python_warnings.warn(
                    f"""good-smell crashed, please open an issue to {ISSUE_LINK} and include the following stack trace:
```py
{get_traceback()}
```
                 """
                )
                continue
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
