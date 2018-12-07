from pathlib import Path

from fire import Fire
from typing import Type, Iterable

from good_smell import LintSmell, RangeLenSmell, NestedFor, SmellWarning


def print_smell_warnings(path: str):
    """Prints any warning messages about smells"""
    print('\n'.join(warning.warning_string()
                    for warning in smell_warnings(Path(path))))


def smell_warnings(path: Path) -> Iterable[SmellWarning]:
    for smell in (NestedFor, RangeLenSmell):
        yield from smell(source_code=path.read_text(), path=str(path)).check_for_smell()


def print_fixed_smell(path: str, starting_line: int = 0, end_line: int = None):
    """Prints a fixed version of `source`"""
    pathlib_path = Path(path)
    source = pathlib_path.read_text()
    print(fix_smell(source, starting_line, end_line))


def fix_smell(source: str, starting_line: int = 0, end_line: int = None, path: str = None) -> str:
    """Returns a fixed version of `source`"""
    smell: Type[LintSmell]
    for smell in (RangeLenSmell, NestedFor):
        source = smell(source, starting_line, end_line).fix_smell()
    return source


def main():
    Fire({'fix': print_fixed_smell, 'warn': print_smell_warnings})


if __name__ == '__main__':
    main()
