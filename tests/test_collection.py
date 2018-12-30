import itertools
from os import PathLike
from pathlib import Path
from typing import Generator, Iterator, List, NamedTuple, TypeVar

import autopep8
import pytest

from good_smell import fix_smell, smell_warnings

FILE_DIR = Path(__file__).parent
EXAMPLES_DIR = FILE_DIR / "examples"


def normalize_formatting(code: str) -> str:
    """Returns a string of the code with normalized formatting for easier compares"""
    return autopep8.fix_code(code, options={"aggressive": 2})


class CollectedTest(NamedTuple):
    desc: str
    before: int
    error_symbols: List[str]
    after: str


def is_title(line: str) -> bool:
    return line.startswith("#:")


T = TypeVar("T")


def repeating_generator(iterator: Iterator[T]) -> Generator[T, T, None]:
    """A generator that can be sent the next item it will yield"""
    sent_item = None
    for item in iterator:
        if sent_item:
            yield sent_item  # Is returned to generator.send
            yield sent_item  # Is returned in the next iteration
        sent_item = yield item


def collect_tests(path: PathLike) -> Iterator[CollectedTest]:
    """Collects all test cases listed in `path`"""
    with open(path) as fp:
        lines = fp.readlines()
    lines_iter = repeating_generator(lines)
    for line in (line for line in lines_iter if is_title(line)):
        desc = line.strip("#:").strip()
        symbols = next(lines_iter).strip("#").strip().split(",")
        before = "".join(itertools.takewhile(lambda l: "==>" not in l, lines_iter))
        after = ""
        for line in lines_iter:
            if is_title(line):
                lines_iter.send(str(line))
                break
            after += line
        yield CollectedTest(
            desc=desc, error_symbols=symbols, before=before, after=after
        )


def test_collect_tests():
    example_path = EXAMPLES_DIR / "example.py"
    collected_tests = list(collect_tests(example_path))
    assert len(collected_tests) == 2
    for case in collected_tests:
        assert case.desc == "example"
        assert case.error_symbols == ["example-symbol", "another-one"]
        assert case.before == """before = 0\nbefore = 1\n"""
        assert case.after == """after = 0\nafter = 1\n"""


def params_from_file():
    f: Path
    for file in (f for f in EXAMPLES_DIR.iterdir() if "example" not in f.name):
        yield from (
            pytest.param(
                case.before,
                case.after,
                case.error_symbols,
                id=str(file) + ":" + case.desc,
            )
            for case in collect_tests(file)
        )


@pytest.mark.parametrize(["before", "after", "symbols"], list(params_from_file()))
def test_collected_items(before, after, symbols):
    assert normalize_formatting(fix_smell(before)) == normalize_formatting(after)
    # assert set(symbols) == {warn.symbol for warn in smell_warnings(before)}
