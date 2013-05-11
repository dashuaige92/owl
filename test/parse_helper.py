import unittest
import ast
import difflib
import warnings

from owl import parse
from owl import transform
from owl.errors import LexError, ParseError, TransformError
import lib.astpp as astpp

class ParserTestCase(unittest.TestCase):
    """A test case that includes helper assertion methods for Owl's parser.
    """
    def assertAST(self, owl_source, python_source):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            owl_tree = parse.parse(owl_source)
            if any(issubclass(e.category, LexError) for e in w):
                raise AssertionError('Unexpected LexError!')
            if any(issubclass(e.category, ParseError) for e in w):
                raise AssertionError(
                    'Unexpected ParseError in Owl source!\n' +
                    '\n'.join(str(e.message) for e in w)
                )

        owl_dump = astpp.dump(owl_tree)

        try:
            python_tree = ast.parse(python_source)
        except SyntaxError:
            raise AssertionError('Unexpected SyntaxError in Python source!')
        python_dump = astpp.dump(python_tree)

        if owl_dump != python_dump:
            diff = '\n'.join(difflib.unified_diff(owl_dump.splitlines(), python_dump.splitlines()))
            raise AssertionError('Generated ASTs are not equal.' +
                                 '\n\nOwl:\n' + owl_dump +
                                 '\n\nPython:\n' + python_dump +
                                 '\n\n' + diff
                                )

    def assertParseError(self, owl_source):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')

            parse.parse(owl_source)
            if any(issubclass(e.category, LexError) for e in w):
                raise AssertionError('Unexpected LexError!')
            if not any(issubclass(e.category, ParseError) for e in w):
                raise AssertionError('Expected ParseError not raised!')

class TransformTestCase(ParserTestCase):
    """An extension of ParserTestCase that performs AST transformation first.
    """
    def assertTransformedAST(self, owl_source, python_source,
                             transform_filters=[transform.StandardLibraryAdder, transform.ScopeResolver]):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')

            # Build the AST and apply transformations.
            owl_tree = parse.parse(owl_source)
            owl_tree = transform.transform(owl_tree, transform_filters)
            if any(issubclass(e.category, LexError) for e in w):
                raise AssertionError('Unexpected LexError!')
            if any(issubclass(e.category, ParseError) for e in w):
                raise AssertionError(
                    'Unexpected ParseError in Owl source!\n' +
                    '\n'.join(str(e.message) for e in w)
                )
            if any(issubclass(e.category, TransformError) for e in w):
                raise AssertionError(
                    'Unexpected TransformError in Owl source!\n' +
                    '\n'.join(str(e.message) for e in w)
                )
        owl_dump = astpp.dump(owl_tree)

        try:
            python_tree = ast.parse(python_source)
        except SyntaxError:
            raise AssertionError('Unexpected SyntaxError in Python source!')
        python_dump = astpp.dump(python_tree)

        if owl_dump != python_dump:
            diff = '\n'.join(difflib.unified_diff(owl_dump.splitlines(), python_dump.splitlines()))
            raise AssertionError('Generated ASTs are not equal.' +
                                 '\n\nOwl:\n' + owl_dump +
                                 '\n\nPython:\n' + python_dump +
                                 '\n\n' + diff
                                )

    def assertTransformError(self, owl_source,
                             transform_filters=[transform.StandardLibraryAdder, transform.ScopeResolver]):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')

            owl_tree = parse.parse(owl_source)
            owl_tree = transform.transform(owl_tree, transform_filters)
            if any(issubclass(e.category, LexError) for e in w):
                raise AssertionError('Unexpected LexError!')
            if any(issubclass(e.category, ParseError) for e in w):
                raise AssertionError(
                    'Unexpected ParseError in Owl source!\n' +
                    '\n'.join(str(e.message) for e in w)
                )
            if not any(issubclass(e.category, TransformError) for e in w):
                raise AssertionError('Expected TransformError not raised!')

    def assertNoTransformError(self, owl_source,
                               transform_filters=[transform.StandardLibraryAdder, transform.ScopeResolver]):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')

            owl_tree = parse.parse(owl_source)
            owl_tree = transform.transform(owl_tree, transform_filters)
            if any(issubclass(e.category, LexError) for e in w):
                raise AssertionError('Unexpected LexError!')
            if any(issubclass(e.category, ParseError) for e in w):
                raise AssertionError(
                    'Unexpected ParseError in Owl source!\n' +
                    '\n'.join(str(e.message) for e in w)
                )
            if any(issubclass(e.category, TransformError) for e in w):
                raise AssertionError(
                    'Unexpected TransformError in Owl source!\n' +
                    '\n'.join(str(e.message) for e in w)
                )
