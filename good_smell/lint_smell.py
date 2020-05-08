import abc
import ast
import os
from typing import List, Optional
from good_smell import SmellWarning


class LintSmell(abc.ABC):
    """Abstract Base class to represent the sniffing instructions for the linter"""

    def __init__(
        self,
        transform: bool,
        path: Optional[str] = None,
        tree: Optional[ast.AST] = None,
    ):
        self.tree = tree
        self.path = path
        self.transform = transform

    @classmethod
    def from_source(
        cls,
        source_code: str,
        transform: bool = True,
        start_line: Optional[int] = 0,
        end_line: Optional[int] = None,
        path: Optional[str] = None,
    ) -> "LintSmell":
        start_line = start_line
        end_line = end_line or len(source_code.splitlines())
        source_code = os.linesep.join(source_code.splitlines()[start_line:end_line])
        return cls(transform=transform, path=path, tree=ast.parse(source_code))

    @abc.abstractmethod
    def check_for_smell(self) -> List[SmellWarning]:
        """Return a list of all occuring smells of this smell class"""

    @abc.abstractmethod
    def fix_smell(self) -> str:
        """Return a fixed version of the code without the code smell"""

    @property
    @abc.abstractmethod
    def symbol(self) -> str:
        """The symbolic name for the smell"""

    @property
    @abc.abstractmethod
    def warning_message(self) -> str:
        """The symbolic name for the smell"""
