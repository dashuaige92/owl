import sys, re
import ast
import ply.yacc as yacc

import lex

tokens = lex.tokens
precedence = (
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
                 | expression NEWLINE
    """
    if len(p) == 2:
        p[0] = None
    elif len(p) == 3:
        p[0] = p[1]

def p_expression(p):
    """expression : function_call
                  | string
                  | number
    """
    p[0] = p[1]

def p_function_call(p):
    """function_call : PRINT LPAREN expression RPAREN
    """
    p[0] = ast.Print(None, [p[3]], True)

def p_initialization(p):
    """initialization : type NAME EQUAL expression
    """
    # need to figure out how to add default values to AST
    # | type NAME

def p_type(p):
    """type : INT
            | BOOL
            | FLOAT
            | STRING
            | LIST
    """

def p_string(p):
    """string : LIT_STRING
    """
    p[0] = ast.Str(p[1][1:-1])

def p_number(p):
    """number : LIT_NUMBER
    """
    p[0] = ast.Num(int(p[1]))

def p_error(p):
    print "Syntax error in input!"

parser = yacc.yacc()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        tree = parser.parse(open(sys.argv[1]).read())
    else:
        tree = parser.parse(sys.stdin.read())
    tree = ast.fix_missing_locations(tree)
    exec compile(tree, '<string>', mode='exec')
