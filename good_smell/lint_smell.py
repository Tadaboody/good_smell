import abc
import ast
import os
from typing import List, Optional
from good_smell import SmellWarning


class LintSmell(abc.ABC):
    """Abstract Base class to represent the sniffing instructions for the linter"""

    def __init__(
        self,
        source_code: Optional[str] = None,
        start_line: Optional[int] = 0,
        end_line: Optional[int] = None,
        path: Optional[str] = None,
        tree: Optional[ast.AST] = None,
    ):
        if source_code:
            self.start_line = start_line
            self.end_line = end_line or len(source_code.splitlines())
            self.source_code = os.linesep.join(
                source_code.splitlines()[start_line:end_line]
            )
        self.tree = tree or ast.parse(self.source_code)

        self.path = path

    @abc.abstractmethod
    def check_for_smell(self) -> List[SmellWarning]:
        """Return a list of all occuring smells of this smell class"""

    @abc.abstractmethod
    def fix_smell(self) -> str:
        """Return a fixed version of the code without the code smell"""

    @property
    @abc.abstractmethod
    def code(self) -> str:
        """ The smell's error code. Of the shape SMLxxx"""
