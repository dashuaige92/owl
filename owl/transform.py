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
                targets=[ast.Name(id=node.name, ctx=ast.Store(), level=node.level)],
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
                ),
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
        fun = ast.FunctionDef(
            name='func_%s' % (node.name,),
            args=ast.arguments([], None, None, []),
            body=node.body if len(node.body) > 0 else [ast.Pass()],
            decorator_list=[],
            #level=node.level,
            globals=node.globals,
        )
        ass = ast.AugAssign(ast.Attribute(ast.Name('%s' % node.name, ast.Load()), 'on_%s' % node.e, ast.Store()), ast.Add(), ast.Name('func_%s' % node.name, ast.Load()))
        return [fun, ass]

    def visit_Transition(self, node):

        if type(node.arg) == list:
            arg_name = "default_transition"
            default = True
        else:
            arg_name = node.arg.s.split()[0]
            default = False
        fun = ast.FunctionDef(
            name='trans_%s_%s_%s' % (node.left, node.right, arg_name),
            args=ast.arguments([], None, None, []),
            body=node.body if len(node.body) > 0 else [ast.Pass()],
            decorator_list=[],
            #level=node.level,
            globals=node.globals,
        )


        if default:
            val = ast.copy_location(ast.Assign(
                    targets=[ast.Name(
                        id='_%s_%s_%s' % (node.left, node.right, arg_name),
                        ctx=ast.Store(),
                    )],
                    value=ast.Call(
                        func=ast.Name(id='Transition', ctx=ast.Load()),
                        args=[
                            ast.Name(id=node.left, ctx=ast.Load()),
                            ast.Name(id=node.right, ctx=ast.Load())
                        ],
                        keywords=[],
                        starargs=None,
                        kwargs=None,
                    )
                    ), node)
        else:
            val = ast.copy_location(ast.Assign(
                targets=[ast.Name(
                    id='_%s_%s_%s' % (node.left, node.right, arg_name),
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
                            ast.Str(s=node.arg.s), # Get value of ast.Str in arg (consider putting .split()[0] here and mention this in the manual
                        ]))
                    ],
                    keywords=[],
                    starargs=None,
                    kwargs=None,
                )
                ), node)


        ass = ast.AugAssign(ast.Attribute(ast.Name('_%s_%s_%s' % (node.left, node.right, arg_name), ast.Load()), 'on_enter', ast.Store()), ast.Add(), ast.Name('trans_%s_%s_%s' % (node.left, node.right, arg_name), ast.Load()))


        transitions.append(val)
        return [fun, val, ass]

class TypeChecker(ast.NodeTransformer): 

    arith_types = set([int, float])
    str_comp = set([ast.Eq, ast.NotEq])


    def visit_Assign(self, node):
        # Assign node must have type set in parse.py
        self.generic_visit(node)
        if node.type != node.value.type:
            warnings.warn("""Cannot assign type %s
                to variable of type %s""" % (str(node.value.type),
                    str(node.type)), TransformError)
        return node

    def visit_Expr(self, node):
        self.generic_visit(node)
        return node

    def visit_BinOp(self, node):
        self.generic_visit(node)

        l_type = node.left.type
        r_type = node.right.type

        if l_type in self.arith_types and r_type in self.arith_types:
            # Valid 
            if l_type == float or r_type == float:
                node.type = float
            else:
                node.type = int
        else:
            warnings.warn("""Invalid Arithmetic Expression: performing Binary Operation
                with types %s and %s""" % (str(l_type), str(r_type)), TransformError)
            node.type = int # Should I not assign this?
        return node

    def visit_Compare(self, node):
        self.generic_visit(node)
        
        node.type = None
        if (len(node.ops) != 1):
            warnings.warn("""Invalid Comparison Expression: Cannot have more than one Comparison
                                            """ % (str(l_type), str(r_type)), TransformError)
        else:
            l_type = node.left.type
            r_type = node.comparators[0].type
            if l_type == str and r_type == str:
                if type(node.ops[0]) in self.str_comp:
                    node.type = bool
            elif l_type in self.arith_types and r_type in self.arith_types:
                node.type = bool
            else:
                 warnings.warn("""Invalid Comparison Expression: performing Comparison 
                        between types %s and %s""" % (str(l_type), str(r_type)), TransformError)
                 node.type = None
        return node

    def visit_BoolOp(self, node):
        self.generic_visit(node)

        node.type = bool
        for val in node.values:
            if val.type != bool:
                node.type = None
                warnings.warn("""Invalid Boolean Expression: Invalid value of type
                                 %s""" % str(val.type), TransformError)
                break

        return node
    def visit_UnaryOp(self, node):
        self.generic_visit(node)

        op_type = node.operand.type
        if type(node.op) == ast.USub:
            if op_type == int:
                node.type = int
            elif op_type == float:
                node.type = float
            else:
                node.type = None
                warnings.warn("""Invalid Unary Minus Expression: Invalid Operand of type
                                                %s""" % str(op_type), TransformError)
        elif type(node.op) == ast.Not:
            if op_type == bool:
                node.type = bool
            else:
                node.type = None
                warnings.warn("""Invalid Unary Not Expression: Invalid Operand of type 
                                                %s""" % (str(op_type)), TransformError)

        return node

    def visit_Name(self, node):
        # Check bool
        if node.id == 'True' or node.id == 'False':
            node.type = bool
        # Other ast.Name nodes
        return node

    def visit_Num(self, node):
        #is the following necessary? We split int and float in parse.py
        if isinstance(node.n, int):
            node.type = int
        elif isinstance(node.n, float):
            node.type = float
        else:
            warnings.warn('%s is not a valid number' % (str(node.n)), TransformError)
        return node

    def visit_Str(self, node):
        if not isinstance(node.s, str):
            warnings.warn('%s is not a valid number' % (str(node.s)), TransformError)

        node.type = str
        return node

    def visit_List(self, node):
        self.generic_visit(node)
        tmp = node.elts
        if any(tmp):
            var_type = tmp[0].type
            # Right now just checking if all types are the same
            for node in tmp:
                if node.type != var_type:
                    warnings.warn("""List entries must be of type %s""" % var_type, 
                                                                TransformError)
                    break
            node.type = list
        return node

class ScopeResolver(ast.NodeTransformer):
    """Add underscores for scopes to avoid naming conflicts.
    Add global keyword when making new function scopes.
    """

    def visit_FunctionDef(self, node):
        self.generic_visit(node)
        if hasattr(node, 'level'):
            node.name = '_'*(node.level + 1) + node.name
        node.body.insert(0, ast.Global(names=['_'*(level+1) + name for level, name in node.globals]))
        return node

    def visit_Name(self, node):
        self.generic_visit(node)
        if hasattr(node, 'level'):
            node.id = '_'*(node.level + 1) + node.id
        return node

def transform(tree, filters=[]):
    for Transformer in [StandardLibraryAdder, TypeChecker, MachineCodeGenerator, ScopeResolver]:
        if Transformer not in filters:
            tree = Transformer().visit(tree)
    tree = ast.fix_missing_locations(tree)
    return tree

def build_tree(args):
    tree = parse.build_tree(args)
    symbol_table = tree.symbol_table
    tree = transform(tree)
    tree.symbol_table = symbol_table
    return tree

def main(args):
    tree = build_tree(sys.argv)
    exec compile(tree, '<string>', mode='exec')

if __name__ == '__main__':
    main(sys.argv)
