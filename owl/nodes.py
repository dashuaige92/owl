import ast

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
