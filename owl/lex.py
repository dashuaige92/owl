import sys
import warnings

import ply.lex as lex

from errors import LexError

# Reserved keywords
reserved = {
    'print'   : 'PRINT',

    'true'    : 'TRUE' ,
    'false'   : 'FALSE' ,

    'int'     : 'INT',
    'bool'    : 'BOOL',
    'float'   : 'FLOAT',
    'string'  : 'STRING',
    'list'    : 'LIST',
    'machine' : 'MACHINE',

    'for'     : 'FOR',
    'in'      : 'IN',
    'while'   : 'WHILE',

    'if'      : 'IF',
    'else'    : 'ELSE',
    'range'   : 'RANGE',
}

tokens = tuple(reserved.values()) + (
    # Literals
    'LIT_STRING', 'LIT_NUMBER',

    # Delimiters
    'LPAREN', 'RPAREN', 'LBRACK', 'RBRACK', 'LBRACE', 'RBRACE', 'COMMA',
    'NEWLINE',
                                    
    # Identifiers
    'NAME',

    # Operators
    'EQUAL',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO',
    'EQ', 'NEQ', 'LT', 'LTEQ', 'GT', 'GTEQ',
    'DOT',
)

t_LIT_STRING = r'\"([^\\\n]|(\\.))*?\"'
t_LIT_NUMBER = r'[0-9]+'

t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACK  = r'\['
t_RBRACK  = r'\]'
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'
t_COMMA   = r','
t_NEWLINE = r'\n'

t_EQUAL   = r'='
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_MODULO  = r'%'
t_EQ      = r'=='
t_NEQ     = r'!='
t_LT      = r'<'
t_LTEQ     = r'<='
t_GT      = r'>'
t_GTEQ     = r'>='
t_DOT     = r'\.'

t_ignore  = ' \t'

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    # Check for reserved keywords
    t.type = reserved.get(t.value, 'NAME')
    return t

def t_error(t):
    warnings.warn("Illegal character '%s'" % t.value[0], LexError)
    t.lexer.skip(1)

lexer = lex.lex()

def main(args):
    if len(args) > 1:
        lexer.input(open(args[1]).read())
    else:
        lexer.input(sys.stdin.read())
    for tok in lexer:
        print tok

if __name__ == '__main__':
    main(sys.argv)
