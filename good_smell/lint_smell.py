import abc
import os

class LintSmell(abc.ABC):
    """A class to represent the sniffing instructions for the linter"""

    def __init__(self, source_code: str, start_line=0, end_line=None):
        self.start_line = start_line
        self.end_line = end_line or len(source_code.splitlines())
        self.source_code = os.linesep.join(source_code.splitlines()[start_line:end_line])

    @abc.abstractmethod
    def check_for_smell(self) -> bool:
        """Check if the smell occurs between `starting_line` and `end_line` in `source_code`"""

    @abc.abstractmethod
    def fix_smell(self) -> str:
        """Return a fixed version of the code without the code smell"""
