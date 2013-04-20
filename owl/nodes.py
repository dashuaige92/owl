import ast

def flatten(seq):
    l = []
    for elt in seq:
        t = type(elt)
        if t is tuple or t is list:
            for elt2 in flatten(elt):
                l.append(elt2)
        else:
            l.append(elt)
    return l

def flatten_nodes(seq):
    return [n for n in flatten(seq) if isinstance(n, ast.AST)]

class Node(ast.stmt):
    _fields = ('name',)

    def __init__(self, name):
        self.name = name

class Transition(ast.stmt):
    _fields = ('left', 'arg', 'right', 'body')

    def __init__(self, left, arg, right, body=[]):
        self.left = left
        self.arg = arg
        self.right = right
        self.body = body

class Machine(ast.stmt):
    _fields = ('name', 'data', 'nodes', 'functions', 'transitions')

    def __init__(self, name, data=[], nodes=[], functions=[], transitions=[]):
        self.name = name
        self.data = data
        self.nodes = nodes
        self.functions = functions
        self.transitions = transitions

# class Int(ast.expr):
#     def __init__(self, *args, **kwargs):
#         ast.Expr.__init__(self, *args, **kwargs)
#         self.type = int

# class Bool(ast.expr):
#     def __init__(self, *args, **kwargs):
#         ast.Expr.__init__(self, *args, **kwargs)
#         self.type = bool

# class Float(ast.expr):
#     def __init__(self, *args, **kwargs):
#         ast.Expr.__init__(self, *args, **kwargs)
#         self.type = float

# class Str(ast.expr):
#     def __init__(self, *args, **kwargs):
#         ast.Expr.__init__(self, *args, **kwargs)
#         self.type = str
# class List(ast.expr):
#     def __init__(self, *args, **kwargs):
#         ast.Expr.__init__(self, *args, **kwargs)
#         self.type = list

