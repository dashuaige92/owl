"""
Usage: python ptree.py [owl-source-file]
       python ptree.py [owl-source-file] > [python-dest-file]
"""

import sys

from owl import parse
from lib import astpp

if __name__ == '__main__':
    tree = parse.build_tree(sys.argv)
    print astpp.dump(tree)
    print 'Symbol table:'
    print tree.symbol_table
