import itertools
import ast
from good_smell.smells import NestedFor


def compare_ast(node1, node2):
    """Compare two ast, adapted from https://stackoverflow.com/a/30581854 to py3"""
    if type(node1) is not type(node2):
        return False
    if isinstance(node1, ast.AST):
        for k, v in vars(node1).items():
            if k in ("lineno", "col_offset", "ctx"):
                continue
            if not compare_ast(v, getattr(node2, k)):
                return False
        return True
    elif isinstance(node1, list):
        return all(itertools.starmap(compare_ast, zip(node1, node2)))
    else:
        return node1 == node2


def test_no_transform():
    source = """
seq_a = [0]
seq_b = range(10)
for i in seq_a:
    for j in seq_b:
        print(i, j)"""
    original_tree = ast.parse(source)
    tree = ast.parse(source)
    assert NestedFor(transform=False, path="test", tree=tree).check_for_smell()

    assert compare_ast(original_tree, tree)
