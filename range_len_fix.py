from astpretty import pprint
from ast import *
import ast


class EnumerateFixer(NodeTransformer):
    def visit_For(self, node: ast.For):
        print("visit")
        if self.is_range_len(node):
            print("found")
            enumerate_node = Name(id='enumerate', ctx=Load())
            node: For
            node_iterable = node.iter.args[0].args[0]
            return ast.fix_missing_locations(copy_location(For(target=Tuple(elts=[Name(id='i', ctx=Store()), Name(id='elm', ctx=Store())], ctx=Store()),
                                                               iter=Call(
                func=enumerate_node, args=[node_iterable], keywords=[]),
                body=node.body,
                orelse=node.orelse), node))
        return node

    @staticmethod
    def is_range_len(node: ast.For):
        try:
            print("check")
            print(pprint(node))
            return node.iter.func.id == 'range' and node.iter.args[0].func.id == 'len'
        except AttributeError as e:
            print("attr error!" + str(e))
            return False
        # if isinstance(node, ast.For):
        #     node: For
        #     iters = node.iter
        #     if isinstance(iters, Call) and iters.func.id == 'range' :
        #         iters_arg = iters.args[0]
        #         return isinstance(iters_arg, Call) and iters_arg.func.id == 'len'


def swap_enumerate(code: str):
    return EnumerateFixer().visit(ast.parse(code))


def main():
    code = """a=[]
for i in range(len(a)):
    pass
        """
    node = swap_enumerate(code)
    pprint(node)
    import astor
    print(astor.to_source(node))


if __name__ == "__main__":
    main()
