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

    arith_types = [int, float]
    concat_types = [str, list]
    str_comp = [ast.Eq, ast.NotEq]
    list_types = [int, float, str, bool]
    float_list = [float, (list, float)]
    int_list = [int, (list, int)]

    def visit_Subscript(self, node):
        self.generic_visit(node)
        node.type = node.value.type[1]
        return node

    def visit_Index(self, node):
        self.generic_visit(node)
        if hasattr(node.value, 'type') and node.value.type is not int:
            warnings.warn("List index must be an integer!", TransformError)
        return node

    def visit_Assign(self, node):
        # Assign node must have type set in parse.py
        self.generic_visit(node)
        if node.type != node.value.type:
            if node.type in self.float_list and node.value.type in self.int_list:
                return node

            warnings.warn("""Cannot assign type %s to variable of type %s""" \
                        % (str(node.value.type), str(node.type)), TransformError)
        return node

    def visit_Expr(self, node):
        self.generic_visit(node)
        return node

    def visit_FunctionDef(self, node):
        self.generic_visit(node)
        for stmt in node.body:
            if isinstance(stmt, ast.Return):
                if stmt.value.type != node.type:
                    warnings.warn("""Function %s must return value of type %s: 
                            have type %s""" % (str(node.name), str(node.type), 
                                             str(stmt.value.type)), TransformError)
            elif hasattr(stmt, 'return_type'):
                for ret_type in stmt.return_type:
                    if ret_type != node.type:
                        warnings.warn("""Function %s must return value of type %s: 
                            have type %s""" % (str(node.name), str(node.type), 
                                             str(ret_type)), TransformError)
        return node
    def visit_Return(self, node):
        self.generic_visit(node)
        return node

    def visit_If(self, node):
        self.generic_visit(node)
        node.return_type = set()
        body = node.body
        if hasattr(node, 'orelse'):
            body += node.orelse
        for stmt in body:
            if isinstance(stmt, ast.Return):
                node.return_type.add(stmt.value.type)
            elif hasattr(stmt, 'return_type'):
                node.return_type.update(stmt.return_type)
        return node

    def visit_While(self, node):
        self.generic_visit(node)
        node.return_type = set()
        for stmt in node.body:
            if isinstance(stmt, ast.Return):
                node.return_type.add(stmt.value.type)
            elif hasattr(stmt, 'return_type'):
                node.return_type.update(stmt.return_type)
        return node

    def visit_For(self, node):
        self.generic_visit(node)
        node.return_type = set()
        if node.target.type != int:
            warnings.warn("""For loop requires value of type int: have value of
                type %s""" % (int, str(node.target.type)), TransformError)
        if node.iter.type != (list, int):
            warnings.warn("""For loop requires a list of values of type int: have
                type %s""" % (str(node.iter.type)), TransformError)
        for stmt in node.body:
            if isinstance(stmt, ast.Return):
                node.return_type.add(stmt.value.type)
            elif hasattr(stmt, 'return_type'):
                node.return_type.update(stmt.return_type)
        return node
    def visit_Call(self, node):
        self.generic_visit(node)
        if hasattr(node, 'type'):
            if node.args[0].type not in self.list_types:
                node.type = None
                warnings.warn("""Typecast requires value of type int, float, bool or string:
                    have type %s""" % (str(node.args[0].type)), TransformError)
        # else:

            # for arg in node.args:
            #     if arg.type != node.type:
            #         node.type = None
            #         warnings.warn(""")

        return node
    
    def visit_Subscript(self, node):
        self.generic_visit(node)
        index_type = node.slice.value.type
        if index_type != int:
            warnings.warn("""Indexing value must be of type int: have 
                type %s""" % (str(index_type)), TransformError)
        return node

#symbol table: get_table, all_names, global_names, local_names, get_type
# check return type
# ast.FunctionDef(name=p[2], args=ast.arguments(args=p[5], vararg=None, 
#    kwarg=None, defaults=[]), body=p[8], decorator_list=[], type=p[1], 
#       level=0, globals=global_names())

 # func(params)
 # ast.Call(func=p[1], \
                # args=p[3], keywords=[], starargs=None, kwargs=None)

# obj.val
# ast.Attribute(value=p[1], attr=p[3], ctx=ast.Load())
# obj must be machine, must have field func? 

# func.name(params)
# ast.Call(func=ast.Attribute(value=p[1], \
  #          attr=p[3], ctx=ast.Load()), args=p[5], keywords=[], starargs=None, kwargs=None)

# list[int]
# ast.Subscript(
#                 value=p[1],
#                 slice=ast.Index(value=p[3]),
#                 ctx=ast.Load(),
#                 )


    def visit_BinOp(self, node):
        self.generic_visit(node)

        l_type = node.left.type
        r_type = node.right.type

        # Numbers
        if l_type in self.arith_types and r_type in self.arith_types:
            if l_type == int and r_type == int:
                node.type = int
            else:
                node.type = float
        # Concatenation of strings and lists
        elif type(node.op) is ast.Add and l_type == r_type and l_type in self.concat_types:
            node.type = l_type
        else:
            warnings.warn("""Invalid Arithmetic Expression: performing Binary Operation
                with types %s and %s""" % (str(l_type), str(r_type)), TransformError)
            node.type = None
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
        # Must load from symbol table?
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
            list_type = tmp[0].type
            for i in tmp:
                if i.type != list_type:
                    if i.type in self.arith_types and \
                    list_type in self.arith_types:
                        list_type = float
                    else:
                        warnings.warn("""List entries must be of type %s""" % list_type, 
                                                                TransformError)
                        list_type = None
                        break
            node.type = (list, list_type)
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

    def visit_Assign(self, node):
        self.generic_visit(node)
        if hasattr(node, 'level'):
            node.targets[0].id = '_'*(node.level + 1) + node.targets[0].id
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
