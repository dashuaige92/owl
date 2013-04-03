import sys, re
import ply.lex as lex

# Reserved keywords
reserved = {
    'print': 'PRINT',
    'true' : 'TRUE' ,
    'false' : 'FALSE' ,
}

tokens = tuple(reserved.values()) + (
    # Literals
    'LIT_STRING', 'LIT_NUMBER', 

    # Delimiters
    'LPAREN', 'RPAREN',

    'NEWLINE',
                                    
    # NEW SECTION
    'NAME'
)

t_LIT_STRING = r'\"([^\\\n]|(\\.))*?\"'
t_LIT_NUMBER = r'[0-9]+'


t_LPAREN  = r'\('
t_RPAREN  = r'\)'

t_NEWLINE = r'\n'

t_ignore  = ' \t'

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    # Check for reserved keywords
    t.type = reserved.get(t.value, 'NAME')
    return t

def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

lexer = lex.lex()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        lexer.input(open(sys.argv[1]).read())
    else:
        lexer.input(sys.stdin.read())
    for tok in lexer:
        print tok
