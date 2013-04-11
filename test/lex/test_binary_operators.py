import unittest

from test.lex_helper import LexerTestCase

class test_binary_operators(LexerTestCase):

    def test_plus(self):
        self.assertTokenTypes(
            '1 + 2',
            ('1', 'LIT_NUMBER'),
            ('+', 'PLUS'),
            ('2', 'LIT_NUMBER'),
        )

    def test_minus(self):
        self.assertTokenTypes(
            '2-1',
            ('2', 'LIT_NUMBER'),
            ('-', 'MINUS'),
            ('1', 'LIT_NUMBER'),
        )

    def test_times(self):
        self.assertTokenTypes(
            '1*2',
            ('1', 'LIT_NUMBER'),
            ('*', 'TIMES'),
            ('2', 'LIT_NUMBER'),
        )

    def test_divide(self):
        self.assertTokenTypes(
            '2/1',
            ('2', 'LIT_NUMBER'),
            ('/', 'DIVIDE'),
            ('1', 'LIT_NUMBER'),
        )
