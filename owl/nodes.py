import ast

class Group(ast.expr):
    """AST Node representing the groups() standard Owl function."""
    _fields = ('index',)

    def __init__(self, index, **kwargs):
        self.index = index
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

class Node(ast.stmt):
    _fields = ('name',)

    def __init__(self, name, **kwargs):
        self.name = name
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

class Function(ast.stmt):
    _fields = ('e', 'name', 'body')

    def __init__(self, e, name, body=[], **kwargs):
        self.e = e
        self.name = name
        self.body = body
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

class Transition(ast.stmt):
    _fields = ('left', 'arg', 'right', 'body')

    def __init__(self, left, arg, right, body=[], **kwargs):
        self.left = left
        self.arg = arg
        self.right = right
        self.body = body
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

class Machine(ast.stmt):
    _fields = ('name', 'body')

    def __init__(self, name, body=[], **kwargs):
        self.name = name
        self.body = body
        for key, value in kwargs.iteritems():
            setattr(self, key, value)
