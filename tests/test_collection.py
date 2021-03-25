import ast
import itertools
from os import PathLike
from pathlib import Path
from typing import Iterator, NamedTuple, Set

import astor
import black
import pytest

from good_smell import fix_smell, smell_warnings

FILE_DIR = Path(__file__).parent
EXAMPLES_DIR = FILE_DIR / "examples"


def normalize_formatting(code: str) -> str:
    """Returns a string of the code with normalized formatting for easier compares"""
    code = astor.to_source(ast.parse(code))
    try:
        return black.format_file_contents(code, line_length=88, fast=True)
    except black.NothingChanged:
        return code


class CollectedTest(NamedTuple):
    desc: str
    error_symbols: Set[str]
    before: int
    after: str


def is_title(line: str) -> bool:
    return line.startswith(TITLE_PREFIX)


TITLE_PREFIX = "#:"
BEFORE_AFTER_SPLITTER = "==>"
END_SYMBOL = "END"
SPECIAL_SYMBOLS = (TITLE_PREFIX, BEFORE_AFTER_SPLITTER, END_SYMBOL)


def collect_tests(path: PathLike) -> Iterator[CollectedTest]:
    """Collects all test cases listed in `path`"""
    with open(path) as fp:
        lines = fp.readlines()
    lines_iter = iter(lines)  # Create iterator for continued iteration
    for line_num, line in enumerate(line for line in lines_iter if is_title(line)):
        desc = line.strip("#:").strip()
        symbols_line = next(lines_iter).strip("#").strip()
        symbols = {symbol for symbol in symbols_line.split(",") if symbol != "None"}
        before = "".join(
            itertools.takewhile(lambda l: BEFORE_AFTER_SPLITTER not in l, lines_iter)
        )
        after = "".join(itertools.takewhile(lambda l: END_SYMBOL not in l, lines_iter))

        collected_test = CollectedTest(
            desc=desc, error_symbols=symbols, before=before, after=after
        )
        if any(
            symbol in field
            for field, symbol in itertools.product(collected_test, SPECIAL_SYMBOLS)
        ):
            raise Exception(
                f"""Wrongly formatted example in {path}:{line_num}
            {collected_test}"""
            )
        yield collected_test


def test_collect_tests():
    example_path = EXAMPLES_DIR / "example.py"
    collected_tests = list(collect_tests(example_path))
    assert len(collected_tests) == 2
    case_with_symbol, case_with_no_symbol = collected_tests
    assert case_with_symbol.desc == "example"
    assert case_with_symbol.error_symbols == {"example-symbol", "another-one"}
    assert case_with_symbol.before == """before = 0\nbefore = 1\n"""
    assert case_with_symbol.after == """after = 0\nafter = 1\n"""

    assert case_with_no_symbol.error_symbols == set()


test_case_files = [f for f in EXAMPLES_DIR.iterdir() if "example" not in f.name]


def params_from_file():
    for file in test_case_files:
        yield from (
            pytest.param(
                case.before,
                case.after,
                case.error_symbols,
                id=f"{file.with_suffix('').name}:{case.desc}",
            )
            for case in collect_tests(file)
        )


@pytest.mark.parametrize(["before", "_", "symbols"], params_from_file())
def test_smell_warning(before, _, symbols):
    assert set(symbols) == {smell.symbol for smell in smell_warnings(before)}


@pytest.mark.parametrize(["before", "after", "_"], list(params_from_file()))
def test_smell_fixing(before, after, _):
    assert normalize_formatting(fix_smell(before)) == normalize_formatting(after)
