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

class Machine(ast.stmt):
    _fields = ('name', 'data', 'nodes', 'functions', 'transitions')

    def __init__(self, name, data=[], nodes=[], functions=[], transitions=[], lineno=None):
        self.name = name
        self.data = data
        self.nodes = nodes
        self.functions = functions
        self.transitions = transitions
        self.lineno = lineno
