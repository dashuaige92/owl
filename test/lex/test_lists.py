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
