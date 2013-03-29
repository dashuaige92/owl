import unittest
import ast

from owl.parse import parser
import lib.astpp as astpp

class ParserTestCase(unittest.TestCase):
    """A test case that includes helper assertion methods for Owl's parser.
    """
    def assertAST(self, owl_source, python_source):
        owl_tree = parser.parse(owl_source)
        owl_dump = astpp.dump(owl_tree)
        python_tree = ast.parse(python_source)
        python_dump = astpp.dump(python_tree)

        if owl_dump != python_dump:
            raise AssertionError('Generated ASTs are not equal.' +
                                 '\n\nOwl:\n' + owl_dump +
                                 '\n\nPython:\n' + python_dump
                                )
