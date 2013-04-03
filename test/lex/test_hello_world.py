import unittest

from test.lex_helper import LexerTestCase

class TestHelloWorld(LexerTestCase):
    def test_hello_world(self):
        self.assertTokens(
            'print("Hello, world!")',
            'print',
            '(',
            '"Hello, world!"',
            ')',
        )
