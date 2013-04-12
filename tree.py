"""
Usage: python tree.py [owl-source-file]
       python tree.py [owl-source-file] > [python-dest-file]
"""

import sys
import ast

from owl.parse import parser
from lib.codegen import to_source
from lib import astpp

if __name__ == '__main__':
    if len(sys.argv) > 1:
        tree = parser.parse(open(sys.argv[1]).read())
    else:
        tree = parser.parse(sys.stdin.read())
    tree = ast.fix_missing_locations(tree)
    print astpp.dump(tree)