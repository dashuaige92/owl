"""
Usage: python run.py [owl-source-file]
"""

import sys
import warnings

from owl import transform

if __name__ == '__main__':
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')

        tree = transform.build_tree(sys.argv)

        if any(issubclass(e.category, Warning) for e in w):
            print 'Errors found in Owl source!'
            for e in w:
                print e.message

        else:
            exec compile(tree, '<string>', mode='exec')
