import sys
import ast
import warnings

import parse
from errors import ParseError

class StandardLibraryAdder(ast.NodeTransformer):
    """Append AST Nodes to mimic a standard library.
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

class MachineCodeGenerator(ast.NodeTransformer):
    """Expand Machine nodes to the builtin AST nodes that define them.
    """
    def visit_Machine(self, node):
        self.generic_visit(node)
        if len(node.nodes) is 0:
            warnings.warn("Machine must declare at least one node!", ParseError)
        statements = node.nodes + [
            ast.copy_location(ast.Assign(
                targets=[ast.Name(id=node.name, ctx=ast.Store())],
                value=ast.Call(
                    func=ast.Name(id='Automaton', ctx=ast.Load()),
                    args=[
                        ast.List(elts=[
                            # nodes.Node already converted to ast.Assign
                            ast.Name(
                                id=assign.targets[0].id,
                                ctx=ast.Load(),
                            ) for assign in node.nodes
                        ], ctx=ast.Load()),
                        ast.List(elts=[], ctx=ast.Load()),
                        ast.Name(id=node.nodes[0].targets[0].id, ctx=ast.Load()),
                    ],
                    keywords=[],
                    starargs=None,
                    kwargs=None,
                )
            ), node)
        ]
        return statements

    def visit_Node(self, node):
        return ast.copy_location(ast.Assign(
            targets=[ast.Name(id=node.name, ctx=ast.Store())],
            value=ast.Call(
                func=ast.Name(id='State', ctx=ast.Load()),
                args=[],
                keywords=[],
                starargs=None,
                kwargs=None,
            )
        ), node)

def build_tree(args):
    tree = parse.build_tree(args)
    tree = StandardLibraryAdder().visit(tree)
    tree = MachineCodeGenerator().visit(tree)
    tree = ast.fix_missing_locations(tree)
    return tree

def main(args):
    tree = build_tree(sys.argv)
    exec compile(tree, '<string>', mode='exec')

if __name__ == '__main__':
    main(sys.argv)
