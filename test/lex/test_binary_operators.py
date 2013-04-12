import unittest

from test.lex_helper import LexerTestCase

class TestBinaryOperators(LexerTestCase):

    def test_plus(self):
        self.assertTokenTypes(
            '1 + 2',
            ('1', 'LIT_NUMBER'),
            ('+', 'PLUS'),
            ('2', 'LIT_NUMBER'),
        )

    def test_minus(self):
        self.assertTokenTypes(
            '2 - 1',
            ('2', 'LIT_NUMBER'),
            ('-', 'MINUS'),
            ('1', 'LIT_NUMBER'),
        )

    def test_times(self):
        self.assertTokenTypes(
            '1 * 2',
            ('1', 'LIT_NUMBER'),
            ('*', 'TIMES'),
            ('2', 'LIT_NUMBER'),
        )

    def test_divide(self):
        self.assertTokenTypes(
            '2 / 1',
            ('2', 'LIT_NUMBER'),
            ('/', 'DIVIDE'),
            ('1', 'LIT_NUMBER'),
        )

    def test_modulo(self):
        self.assertTokenTypes(
            '2 % 1',
            ('2', 'LIT_NUMBER'),
            ('%', 'MODULO'),
            ('1', 'LIT_NUMBER'),
        )

    def test_eq(self):
        self.assertTokenTypes(
            '2 == 1',
            ('2', 'LIT_NUMBER'),
            ('==', 'EQ'),
            ('1', 'LIT_NUMBER'),
        )

    def test_neq(self):
        self.assertTokenTypes(
            '2 != 1',
            ('2', 'LIT_NUMBER'),
            ('!=', 'NEQ'),
            ('1', 'LIT_NUMBER'),
        )

    def test_lt(self):
        self.assertTokenTypes(
            '2 < 1',
            ('2', 'LIT_NUMBER'),
            ('<', 'LT'),
            ('1', 'LIT_NUMBER'),
        )

    def test_lteq(self):
        self.assertTokenTypes(
            '2 <= 1',
            ('2', 'LIT_NUMBER'),
            ('<=', 'LTEQ'),
            ('1', 'LIT_NUMBER'),
        )

    def test_gt(self):
        self.assertTokenTypes(
            '2 > 1',
            ('2', 'LIT_NUMBER'),
            ('>', 'GT'),
            ('1', 'LIT_NUMBER'),
        )

    def test_gteq(self):
        self.assertTokenTypes(
            '2 >= 1',
            ('2', 'LIT_NUMBER'),
            ('>=', 'GTEQ'),
            ('1', 'LIT_NUMBER'),
        )

    def test_multiple_operators(self):
        self.assertTokenTypes(
            '2 >>== 1',
            ('2', 'LIT_NUMBER'),
            ('>', 'GT'),
            ('>=', 'GTEQ'),
            ('=', 'EQUAL'),
            ('1', 'LIT_NUMBER'),
        )

