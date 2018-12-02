from pathlib import Path
from good_smell import fix_smell
from re import match
import pytest
import logging
import autopep8

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


examples = [
    ("""seq = [0]
for i in range(len(seq)):
    a = seq[i]
    print(a)
    """,
     """seq = [0]
for i, a in enumerate(seq):
    print(a)
"""
     ),
    # Replace an empty body with pass
    ("""seq = [0]
for i in range(len(seq)):
    a = seq[i]
    """,
     """seq = [0]
for i, a in enumerate(seq):
    pass
"""
     ),
    # As seen on the README
    ("""for i in range(len(sequence)):
    x = sequence[i]
    do_thing(x,i)""",
     """for i, x in enumerate(sequence):
    do_thing(x, i)
"""),
    ("""for i in range(len(sequence)):
    x = sequence[i]
    do_thing(x,i)""",
     """for i,x in enumerate(sequence):
    do_thing(x, i)
"""),
]


def normalize_formatting(code: str) -> str:
    """Returns a string of the code with normalized formatting (spaces,indents,newlines) for easier compares"""
    return autopep8.fix_code(code, options={"aggressive": 2})


@pytest.mark.parametrize("source,fixed_source", examples)
def test_range_len_assert_fix(source, fixed_source):
    assert normalize_formatting(
        fix_smell(source)) == normalize_formatting(fixed_source)
