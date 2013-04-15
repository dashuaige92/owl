"""
Usage: python tree.py [owl-source-file]
       python tree.py [owl-source-file] > [python-dest-file]
"""

import sys
import ast

from owl import transform
from lib.codegen import to_source
from lib import astpp

if __name__ == '__main__':
    tree = transform.build_tree(sys.argv)
    print astpp.dump(tree)
