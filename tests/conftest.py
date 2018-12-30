from os import PathLike
import itertools
from typing import Generator, Iterator, List, NamedTuple, TypeVar

import autopep8


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
