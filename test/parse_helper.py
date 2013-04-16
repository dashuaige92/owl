import unittest
import ast
import warnings

from owl.parse import parser
from owl import transform
from owl.errors import ParseError, TransformError
import lib.astpp as astpp

class ParserTestCase(unittest.TestCase):
    """A test case that includes helper assertion methods for Owl's parser.
    """
    def assertAST(self, owl_source, python_source):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            owl_tree = parser.parse(owl_source)
            if any(issubclass(e.category, ParseError) for e in w):
                raise AssertionError('Unexpected ParseError in Owl source!')
        owl_dump = astpp.dump(owl_tree)

        try:
            python_tree = ast.parse(python_source)
        except SyntaxError:
            raise AssertionError('Unexpected SyntaxError in Python source!')
        python_dump = astpp.dump(python_tree)

        if owl_dump != python_dump:
            raise AssertionError('Generated ASTs are not equal.' +
                                 '\n\nOwl:\n' + owl_dump +
                                 '\n\nPython:\n' + python_dump
                                )

    def assertParseError(self, owl_source):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')

            parser.parse(owl_source)
            if not any(issubclass(e.category, ParseError) for e in w):
                raise AssertionError('Expected ParseError not raised!')

class TransformTestCase(ParserTestCase):
    """An extension of ParserTestCase that performs AST transformation first.
    """
    def assertTransformedAST(self, owl_source, python_source,
                             transform_filters=[transform.StandardLibraryAdder]):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')

            # Build the AST and apply transformations.
            owl_tree = parser.parse(owl_source)
            owl_tree = transform.transform(owl_tree, transform_filters)
            if any(issubclass(e.category, ParseError) for e in w):
                raise AssertionError('Unexpected ParseError in Owl source!')
            if any(issubclass(e.category, TransformError) for e in w):
                raise AssertionError('Unexpected TransformError in Owl source!')
        owl_dump = astpp.dump(owl_tree)

        try:
            python_tree = ast.parse(python_source)
        except SyntaxError:
            raise AssertionError('Unexpected SyntaxError in Python source!')
        python_dump = astpp.dump(python_tree)

        if owl_dump != python_dump:
            raise AssertionError('Generated ASTs are not equal.' +
                                 '\n\nOwl:\n' + owl_dump +
                                 '\n\nPython:\n' + python_dump
                                )

    def assertTransformError(self, owl_source):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')

            owl_tree = parser.parse(owl_source)
            owl_tree = transform.transform(owl_tree)
            if any(issubclass(e.category, ParseError) for e in w):
                raise AssertionError('Unexpected ParseError in Owl source!')
            if not any(issubclass(e.category, TransformError) for e in w):
                raise AssertionError('Expected TransformError not raised!')
