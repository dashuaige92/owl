"""
Usage: python lex.py [owl-source-file]
"""

import sys

from owl.lex import lexer

def main(args):
    if len(args) > 1:
        lexer.input(open(args[1]).read())
    else:
        lexer.input(sys.stdin.read())
    for tok in lexer:
        print tok

if __name__ == '__main__':
    main(sys.argv)
