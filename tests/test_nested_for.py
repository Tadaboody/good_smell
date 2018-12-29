import pytest

from good_smell import fix_smell
from tests import normalize_formatting

examples = [
    (
        """seq_a = [0]
seq_b = range(10)
for i in seq_a:
    for j in seq_b:
        print(i,j)
    """,
        """seq_a = [0]
seq_b = range(10)
import itertools
for i, j in itertools.product(seq_a, seq_b):
    print(i, j)
""",
    ),
    # Don't work if there's code between the loops (no way to know if it's unsafe)
    (
        """for i in seq_a:
    print(i)
    for j in seq_b:
        print(i,j)
    """,
        """for i in seq_a:
    print(i)
    for j in seq_b:
        print(i,j)
    """,
    ),
    # Don't work if there's code after the nested for
    (
        """for i in seq_a:
    for j in seq_b:
        print(i,j)
    print(i)
    """,
        """for i in seq_a:
    for j in seq_b:
        print(i,j)
    print(i)
    """,
    ),
]


@pytest.mark.parametrize("source,fixed_source", examples)
def test_range_len_assert_fix(source, fixed_source):
    assert normalize_formatting(fix_smell(source)) == normalize_formatting(fixed_source)
