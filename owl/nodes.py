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
    _fields = ('name', 'body')

    def __init__(self, name, body=[]):
        self.name = name
        self.body = body

