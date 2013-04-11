import unittest

from test.lex_helper import LexerTestCase

class TestLiterals(LexerTestCase):

    def test_string_literal(self):
        self.assertTokenTypes(
            'print("Hello, world!")',
            ('print', 'PRINT'),
            ('(', 'LPAREN'),
            ('"Hello, world!"', 'LIT_STRING'),
            (')', 'RPAREN'),
        )

    def test_int_literal(self):
        self.assertTokenTypes(
            'print(3)',
            ('print', 'PRINT'),
            ('(', 'LPAREN'),
            ('3', 'LIT_NUMBER'),
            (')', 'RPAREN'),
        )
