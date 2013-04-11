import unittest

from test.lex_helper import LexerTestCase

class TestHelloWorld(LexerTestCase):

    def test_hello_world(self):
        self.assertTokenTypes(
            'print("Hello, world!")',
            ('print', 'PRINT'),
            ('(', 'LPAREN'),
            ('"Hello, world!"', 'LIT_STRING'),
            (')', 'RPAREN'),
        )
