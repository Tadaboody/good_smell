import os
from pathlib import Path

import pytest

from good_smell import fix_smell, smell_warnings
from tests import CollectedTest, collect_tests, normalize_formatting

FILE_DIR = Path(__file__).parent
EXAMPLES_DIR = FILE_DIR / "examples"


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
