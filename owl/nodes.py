import ast

class Node(ast.stmt):
    _fields = ('name',)

    def __init__(self, name):
        self.name = name

class Function(ast.stmt):
    _fields = ('e', 'name', 'body')

    def __init__(self, e, name, body=[]):
        self.e = e
        self.name = name
        self.body = body

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

