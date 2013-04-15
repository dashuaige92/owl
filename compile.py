"""
Usage: python compile.py [owl-source-file]
       python compile.py [owl-source-file] > [python-dest-file]
"""

import sys
import ast

from owl import transform
from lib.codegen import to_source

if __name__ == '__main__':
    tree = transform.build_tree(sys.argv)
    print to_source(tree)
