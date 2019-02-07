import ast
from good_smell.smells.iterator_map import ASTComperator
import pytest


@pytest.mark.parametrize(
    "module_str",
    [
        "a=3;a=3",
        "f(a,b,foo=1);f(a,b,foo=1)",
        "lambda a:foo(1);lambda a:foo(1)",
        "for i in range(10):print(foo)\nfor i in range(10):print(foo)",
    ],
)
def test_cmp(module_str):
    module = ast.parse(module_str)
    assert ASTComperator().compare(module.body[0], module.body[1])
    assert ASTComperator().compare(module.body[0], module.body[1])
