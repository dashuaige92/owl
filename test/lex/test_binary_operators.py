import unittest

from test.lex_helper import LexerTestCase

class TestBinaryOperators(LexerTestCase):

    def test_plus(self):
        self.assertTokenTypes(
            '1 + 2',
            ('1', 'LIT_INT'),
            ('+', 'PLUS'),
            ('2', 'LIT_INT'),
        )

    def test_minus(self):
        self.assertTokenTypes(
            '2 - 1',
            ('2', 'LIT_INT'),
            ('-', 'MINUS'),
            ('1', 'LIT_INT'),
        )

    def test_times(self):
        self.assertTokenTypes(
            '1 * 2',
            ('1', 'LIT_INT'),
            ('*', 'TIMES'),
            ('2', 'LIT_INT'),
        )

    def test_divide(self):
        self.assertTokenTypes(
            '2 / 1',
            ('2', 'LIT_INT'),
            ('/', 'DIVIDE'),
            ('1', 'LIT_INT'),
        )

    def test_modulo(self):
        self.assertTokenTypes(
            '2 % 1',
            ('2', 'LIT_INT'),
            ('%', 'MODULO'),
            ('1', 'LIT_INT'),
        )

    def test_eq(self):
        self.assertTokenTypes(
            '2 == 1',
            ('2', 'LIT_INT'),
            ('==', 'EQ'),
            ('1', 'LIT_INT'),
        )

    def test_neq(self):
        self.assertTokenTypes(
            '2 != 1',
            ('2', 'LIT_INT'),
            ('!=', 'NEQ'),
            ('1', 'LIT_INT'),
        )

    def test_lt(self):
        self.assertTokenTypes(
            '2 < 1',
            ('2', 'LIT_INT'),
            ('<', 'LT'),
            ('1', 'LIT_INT'),
        )

    def test_lteq(self):
        self.assertTokenTypes(
            '2 <= 1',
            ('2', 'LIT_INT'),
            ('<=', 'LTEQ'),
            ('1', 'LIT_INT'),
        )

    def test_gt(self):
        self.assertTokenTypes(
            '2 > 1',
            ('2', 'LIT_INT'),
            ('>', 'GT'),
            ('1', 'LIT_INT'),
        )

    def test_gteq(self):
        self.assertTokenTypes(
            '2 >= 1',
            ('2', 'LIT_INT'),
            ('>=', 'GTEQ'),
            ('1', 'LIT_INT'),
        )

    def test_multiple_operators(self):
        self.assertTokenTypes(
            '2 >>== 1',
            ('2', 'LIT_INT'),
            ('>', 'GT'),
            ('>=', 'GTEQ'),
            ('=', 'EQUAL'),
            ('1', 'LIT_INT'),
        )

