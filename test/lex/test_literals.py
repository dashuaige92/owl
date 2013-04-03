import unittest

from test.lex_helper import LexerTestCase

class TestLiterals(LexerTestCase):
    def test_string_literal(self):
        self.assertTokens('print("Hello, world!")',
                          'print',
                          '(',
                          '"Hello, world!"',
                          ')',
                         )
    def test_int_literal(self):
        self.assertTokens('print(3)',
                          'print',
                          '(',
                          '3',
                          ')',
                         )                                       