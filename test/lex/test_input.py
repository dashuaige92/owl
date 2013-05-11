import unittest

from test.lex_helper import LexerTestCase

class TestInput(LexerTestCase):

    def test_input(self):
        self.assertTokenTypes(
            'input("enter whatever")',
            ('input', 'INPUT'),
            ('(', 'LPAREN'),
            ('"enter whatever"', 'LIT_STRING'),
            (')', 'RPAREN'),
        )