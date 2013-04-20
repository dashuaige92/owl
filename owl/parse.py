import sys
import ast
import warnings

import ply.yacc as yacc

import lex
import nodes
from errors import ParseError

tokens = lex.tokens
precedence = (
    ('left', 'EQ', 'NEQ', 'LT', 'LTEQ', 'GT', 'GTEQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),
)

def p_program(p):
    """program : code_block
    """
    p[0] = ast.Module(p[1])

def p_code_block(p):
    """code_block : statement
                  | code_block statement
    """
    if len(p) == 2:
        p[0] = [p[1]] if p[1] is not None else []
    elif len(p) == 3:
        p[0] = p[1] + ([p[2]] if p[2] is not None else [])

def p_statement(p):
    """statement : NEWLINE
                 | initialization NEWLINE
                 | iteration
                 | selection_statement
                 | machine
    """
    if p[1] == "\n":
        p[0] = None
    else:
        p[0] = p[1]

# Python only wraps an expression with Expr when it is its own statement
def p_statement_expression(p):
    """statement : expression NEWLINE
    """
    p[0] = p[1] if type(p[1]) is ast.Print else ast.Expr(value=p[1])

def p_expression(p):
    """expression : function_call
                  | arithmetic_expression
                  | comparison_expression
                  | string
                  | number
                  | bool
                  | variable_load
                  | list
    """
    p[0] = p[1]

def p_arithmetic_expression(p):
    """arithmetic_expression : expression PLUS expression
                             | expression MINUS expression
                             | expression TIMES expression
                             | expression DIVIDE expression
                             | expression MODULO expression
    """
    operators = {
        '+': ast.Add(),
        '-': ast.Sub(),
        '*': ast.Mult(),
        '/': ast.Div(),
        '%': ast.Mod(),
    }
    p[0] = ast.BinOp(
        left=p[1],
        op=operators[p[2]],
        right=p[3])

def p_comparison_expression(p):
    """comparison_expression : expression EQ expression
                             | expression NEQ expression
                             | expression LT expression
                             | expression LTEQ expression
                             | expression GT expression
                             | expression GTEQ expression
    """
    operators = {
        '==': ast.Eq(),
        '!=': ast.NotEq(),
        '<': ast.Lt(),
        '<=': ast.LtE(),
        '>': ast.Gt(),
        '>=': ast.GtE(),
    }
    p[0] = ast.Compare(
        left=p[1],
        ops=[operators[p[2]]],
        comparators=[p[3]])

def p_iteration(p):
    """iteration : WHILE LPAREN expression RPAREN LBRACE statement_list RBRACE
                 | FOR variable_store IN variable_load LBRACE statement_list RBRACE
    """

    if p[1] == "while":
        p[0] = ast.While(p[3], p[6], [])
    else:
        p[0] = ast.For(p[2], p[4], p[6], [])

def p_selection_statement(p):
    """selection_statement : IF LPAREN expression RPAREN LBRACE statement_list RBRACE
                           | IF LPAREN expression RPAREN LBRACE statement_list RBRACE ELSE LBRACE statement_list RBRACE
    """

    if len(p) == 8:
        p[0] = ast.If(p[3], p[6], [])
    else:
        p[0] = ast.If(p[3], p[6], p[10])

def p_statement_list(p):
    """statement_list : statement
                      | statement statement_list
    """

    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        if p[1] is not None:
            p[0] = p[1] + ([p[2]] if p[2] is not None else [])
        else:
            p[0] = ([p[2]] if p[2] is not None else [])

def p_function_call(p):
    """function_call : PRINT LPAREN expression RPAREN
                     | NAME LPAREN parameters RPAREN
                     | NAME DOT NAME LPAREN parameters RPAREN
                     | NAME DOT NAME
                     | NAME LBRACK LIT_INT RBRACK

    """
    if p[1] == 'print':
        p[0] = ast.Print(None, [p[3]], True)
    elif len(p) == 4:
        p[0] = ast.Attribute(value=ast.Name(id=p[1], ctx=ast.Load()), attr=p[3], ctx=ast.Load())
    elif len(p) == 7:
        p[0] = ast.Call(func=ast.Attribute(value=ast.Name(id=p[1], ctx=ast.Load()), \
            attr=p[3], ctx=ast.Load()), args=p[5], keywords=[], starargs=None, kwargs=None)
    elif len(p) == 5:
        if p[2] == '[':
            p[0] = ast.Subscript(value=ast.Name(id=p[1], ctx=ast.Load()), \
                slice=ast.Index(value=ast.Num(n=int(p[3]))), ctx=ast.Load())
        elif p[2] == '(':
            p[0] = ast.Call(func=ast.Name(id=p[1], ctx=ast.Load()), \
                args=p[3], keywords=[], starargs=None, kwargs=None)
        # Owl doesn't have keyword arguments, *args, or *kwargs


def p_parameters(p):
    """parameters    : expression
                     | expression COMMA parameters
    """
    # How to have one list and add all parameters to it across multiple reductions?
    #i.e. test(1, 2, 3, 4, 5...)
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        tmp = list(p[3])
        tmp.insert(0, p[1])
        p[0] = tmp

def p_initialization(p):
    """initialization : type variable_store EQUAL expression
                      | type variable_store
    """

    if len(p) == 3:
        # this is for default initialization


        if p[1] == int:
            p[0] = ast.Assign([p[2]], ast.Num(0), type=int)

                
        elif p[1] == bool:
            p[0] = ast.Assign([p[2]], ast.Name("False", ast.Load()),
                type=bool)
                
        elif p[1] == float:
            p[0] = ast.Assign([p[2]], ast.Num(0), type=float)

        elif p[1] == str:
            p[0] = ast.Assign([p[2]], ast.Str(""), type=str)
                
        elif p[1] == list:
            p[0] = ast.Assign([p[2]], ast.List([], ast.Load()), type=list) #check correctness

        else:
            print("%s err" % (str(p[1])))
        


    else:
          #add type checking here
          p[0] = ast.Assign([p[2]], p[4], type=p[1])


def p_type(p):
    """type : INT
            | BOOL
            | FLOAT
            | STRING
            | LIST
    """


    if p[1] == 'int':
        p[0] = int
    elif p[1] == 'bool':
        p[0] = bool
    elif p[1] == 'float':
        p[0] = float
    elif p[1] == 'string':
        p[0] = str
    elif p[1] == 'list':
        p[0] = list
  

def p_number_int(p):
    """number : LIT_INT
    """
    p[0] = ast.Num(int(p[1]))

def p_number_float(p):
    """number : LIT_FLOAT
    """

    p[0] = ast.Num(float(p[1]))

def p_string(p):
    """string : LIT_STRING
    """
    p[0] = ast.Str(p[1][1:-1])


def p_list(p):
    """list : LBRACK parameters RBRACK
            | RANGE LPAREN number RPAREN
            | RANGE LPAREN number COMMA number RPAREN
    """
    if p[1] == '[':
        p[0] = ast.List(p[2], ast.Load())

    elif p[1] == 'range' and p[4] == ',':
        p[0] = value=ast.Call(func=ast.Name(id=p[1], ctx=ast.Load()), args=[
        p[3],p[5]
      ], keywords=[], starargs=None, kwargs=None)

    else:
        p[0] = value=ast.Call(func=ast.Name(id=p[1], ctx=ast.Load()), args=[
        p[3],
      ], keywords=[], starargs=None, kwargs=None)

def p_bool(p):
    """bool : TRUE
            | FALSE
    """
    if p[1] == "true":
        p[0] = ast.Name("True", ast.Load())
    else:
        p[0] = ast.Name("False", ast.Load())

def p_variable_store(p):
    """variable_store : NAME
    """
    p[0] = ast.Name(p[1], ast.Store())

def p_variable_load(p):
    """variable_load : NAME
        """
    p[0] = ast.Name(p[1], ast.Load())

def p_machine(p):
    """machine : MACHINE NAME EQUAL LBRACE machine_body RBRACE
    """
    p[0] = nodes.Machine(p[2], **p[5])

def p_machine_body(p):
    """machine_body : node_decs transitions
    """
    p[0] = {
        'nodes': p[1],
        'transitions': p[2],
    }

def p_node_decs(p):
    """node_decs : node
                 | node_decs node
    """
    if len(p) == 2:
        p[0] = [p[1]] if p[1] is not None else []
    elif len(p) == 3:
        p[0] = p[1] + ([p[2]] if p[2] is not None else [])

def p_node(p):
    """node : NODE NAME NEWLINE
            | NEWLINE
    """
    p[0] = None if len(p) is 2 else nodes.Node(p[2])

def p_transitions(p):
    """transitions : transition
                   | transitions transition
    """
    if len(p) == 2:
        p[0] = [p[1]] if p[1] is not None else []
    elif len(p) == 3:
        p[0] = p[1] + ([p[2]] if p[2] is not None else [])

def p_transition(p):
    """transition : NAME LPAREN string RPAREN ARROW NAME NEWLINE
                  | NAME LPAREN string RPAREN ARROW NAME LBRACE statement_list RBRACE
                  |
    """
    if len(p) == 8:
        p[0] = nodes.Transition(left=p[1], arg=p[3], right=p[6], body=[])
    elif len(p) == 10:
        p[0] = nodes.Transition(left=p[1], arg=p[3], right=p[6], body=p[8])

def p_empty(p):
    """empty :
    """
    pass

def p_error(p):
    warnings.warn("Syntax error on line %d!" % p.lineno, ParseError)

parser = yacc.yacc()

def build_tree(args):
    """Build an AST tree from expected command line args.

    args[0] = script name
    args[1] = <filename>
    args[1] = None for reading stdin.
    """
    if len(args) > 1:
        tree = parser.parse(open(args[1]).read())
    else:
        tree = parser.parse(sys.stdin.read())
    tree = ast.fix_missing_locations(tree)
    return tree

def main(args):
    tree = build_tree(args)
    exec compile(tree, '<string>', mode='exec')

if __name__ == '__main__':
    main(sys.argv)
