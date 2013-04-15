"""
Usage: python run.py [owl-source-file]
"""

import sys

from owl import transform

if __name__ == '__main__':
    tree = transform.build_tree(sys.argv)
    exec compile(tree, '<string>', mode='exec')
