from good_smell import fix_smell
from re import match
import pytest

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
