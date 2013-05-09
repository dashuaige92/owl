import unittest

from test.lex_helper import LexerTestCase

class TestLiterals(LexerTestCase):

    def test_string_literal(self):
        self.assertTokenTypes(
            '"Hello, world!"',
            ('"Hello, world!"', 'LIT_STRING'),
        )
    def test_int_literal(self):
        self.assertTokenTypes(
            '3',
            ('3', 'LIT_INT'),
        )

    def test_float_literal(self):
        self.assertTokenTypes(
            '3.0',
            ('3.0', 'LIT_FLOAT'),
        )

    def test_float_literal_without_integral_part(self):
        self.assertTokenTypes(
            '.0',
            ('.0', 'LIT_FLOAT'),
        )

    def test_float_literal_without_fractional_part(self):
        self.assertTokenTypes(
            '3.',
            ('3.', 'LIT_FLOAT'),
        )
