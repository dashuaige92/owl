import unittest

from test.lex_helper import LexerTestCase

class TestLists(LexerTestCase):
    def test_lists(self):
        self.assertTokenTypes(
            '["Andrew"]',
            ('[', 'LBRACK'),
            ('"Andrew"','LIT_STRING'),
            (']','RBRACK'),
        )

    def test_range(self):
        self.assertTokenTypes(
            'range(3,5)',
            ('range', 'RANGE'),
            ('(', 'LPAREN'),
            ('3', 'LIT_INT'),
            (',', 'COMMA'),
            ('5', 'LIT_INT'),
            (')','RPAREN'),
        )