from pathlib import Path
from typing import Iterable, Type

from fire import Fire

from good_smell import LintSmell, SmellWarning, implemented_smells


def print_smell_warnings(path: str):
    """Prints any warning messages about smells"""
    print(
        "\n".join(
            warning.warning_string()
            for warning in smell_warnings(Path(path).read_text(), path)
        )
    )


def smell_warnings(source: str, path: str = "") -> Iterable[SmellWarning]:
    for smell in implemented_smells:
        yield from smell.from_source(
            source_code=source, path=str(path), transform=False
        ).check_for_smell()


def print_fixed_smell(path: str, starting_line: int = 0, end_line: int = None):
    """Prints a fixed version of `source`"""
    pathlib_path = Path(path)
    source = pathlib_path.read_text()
    print(fix_smell(source, starting_line, end_line))


def fix_smell(
    source: str, starting_line: int = 0, end_line: int = None, path: str = None
) -> str:
    """Returns a fixed version of `source`"""
    smell: Type[LintSmell]
    for smell in implemented_smells:
        source = smell.from_source(
            source_code=source,
            start_line=starting_line,
            end_line=end_line,
            path=path,
            transform=True,
        ).fix_smell()
    return source


def main():
    Fire({"fix": print_fixed_smell})


if __name__ == "__main__":
    main()
