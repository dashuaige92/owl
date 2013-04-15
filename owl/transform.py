import sys
import ast

import parse

class StandardLibraryAdder(ast.NodeTransformer):
    """Append AST Nodes to mimic a standard library
    """

    def visit_Module(self, node):
        imports = [
            ast.ImportFrom(
                module='lib.automata',
                names=[ast.alias(name='*', asname=None)],
                level=0,
            )
        ]
        return ast.copy_location(ast.Module(
            body=imports + node.body
        ), node)

def build_tree(args):
    tree = parse.build_tree(args)
    tree = StandardLibraryAdder().visit(tree)
    tree = ast.fix_missing_locations(tree)
    return tree

def main(args):
    tree = build_tree(sys.argv)
    exec compile(tree, '<string>', mode='exec')

if __name__ == '__main__':
    main(sys.argv)
