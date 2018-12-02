from pathlib import Path

import astor
from fire import Fire

from good_smell import LintSmell, RangeLenSmell, NestedFor


def print_fixed_smell(path: str, starting_line: int = 0, end_line: int = None):
    """Prints a fixed version of `source`"""
    path = Path(path)
    source = path.read_text()
    print(fix_smell(source, starting_line, end_line))


def fix_smell(source: str, starting_line: int = 0, end_line: int = None) -> str:
    """Returns a fixed version of `source`"""
    smell: LintSmell
    for smell in (RangeLenSmell, NestedFor):
        source = smell(source, starting_line, end_line).fix_smell()
    return source


def main():
    Fire(print_fixed_smell)


if __name__ == '__main__':
    main()
