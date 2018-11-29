from pathlib import Path
from iter_lint import fix_smell
from re import match
import pytest
import logging

valid_sources = ["""
a = [0]
for i in range(len(a)):
    print(a[i])
""",
                 """
b = [1]
for i in range(len(a + b)):
    print(i)
"""]


@pytest.mark.parametrize("source", valid_sources)
def test_range_len_fix(source):
    assert not match(r'for \w+ in range\(len\(.+\)\):',
                     fix_smell(source))


def test_range_len_assert_fix():
    source = """seq = [0]
for i in range(len(seq)):
    a = seq[i]
    print(a)
    """
    fixed_source = """seq = [0]
for i, a in enumerate(seq):
    print(a)
""" #TODO: Normalize tests for formatting
    fixed_smell = fix_smell(source)
    assert fix_smell(source) == fixed_source


def test_empty_body():
    """Assert that when creating an empty body it is subsituted with pass"""
    source = """seq = [0]
for i in range(len(seq)):
    a = seq[i]
    """
    fixed_source = """seq = [0]
for i, a in enumerate(seq):
    pass
"""
    assert fix_smell(source) == fixed_source

