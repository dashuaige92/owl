import sys
import ast
import warnings

import lib.astpp as astpp

import parse
from errors import TransformError


nodes = []
transitions = []

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

        nodes[:] = []
        transitions[:] = []

        self.generic_visit(node)
        
        if len(nodes) is 0:
            warnings.warn("Machine must declare at least one node!", TransformError)
            return node
                
        statements = node.body + [
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
                            ) for assign in nodes
                        ], ctx=ast.Load()),
                        ast.List(elts=[
                            # nodes.Transition already converted to ast.Assign
                            ast.Name(
                                id=assign.targets[0].id,
                                ctx=ast.Load(),
                            ) for assign in transitions
                        ], ctx=ast.Load()),
                        ast.Name(id=nodes[0].targets[0].id, ctx=ast.Load()),
                    ],
                    keywords=[],
                    starargs=None,
                    kwargs=None,
                )
            ), node)
        ]

        return statements

    def visit_Node(self, node):

        val = ast.copy_location(ast.Assign(
            targets=[ast.Name(id=node.name, ctx=ast.Store())],
            value=ast.Call(
                func=ast.Name(id='State', ctx=ast.Load()),
                args=[],
                keywords=[],
                starargs=None,
                kwargs=None,
            )
        ), node)
        nodes.append(val)
        return val


    def visit_Function(self, node):
        pass

    def visit_Transition(self, node):
        val = ast.copy_location(ast.Assign(
            targets=[ast.Name(
                id='_%s_%s' % (node.left, node.right),
                ctx=ast.Store(),
            )],
            value=ast.Call(
                func=ast.Name(id='Transition', ctx=ast.Load()),
                args=[
                    ast.Name(id=node.left, ctx=ast.Load()),
                    ast.Name(id=node.right, ctx=ast.Load()),
                    ast.Lambda(args=ast.arguments(args=[
                        ast.Name(id='_x', ctx=ast.Param()),
                    ], vararg=None, kwarg=None, defaults=[]), body=ast.Compare(left=ast.Name(id='_x', ctx=ast.Load()), ops=[
                        ast.Eq(),
                    ], comparators=[
                        ast.Str(s=node.arg.s), # Get value of ast.Str in arg
                    ]))
                ],
                keywords=[],
                starargs=None,
                kwargs=None,
            )
        ), node)
        transitions.append(val)
        return val

def transform(tree, filters=[]):

    for Transformer in [StandardLibraryAdder, MachineCodeGenerator]:
        if Transformer not in filters:
            tree = Transformer().visit(tree)
    tree = ast.fix_missing_locations(tree)
    return tree

def build_tree(args):
    tree = parse.build_tree(args)
    tree = transform(tree)
    return tree

def main(args):
    tree = build_tree(sys.argv)
    exec compile(tree, '<string>', mode='exec')

if __name__ == '__main__':
    main(sys.argv)
