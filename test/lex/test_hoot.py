import unittest

from test.lex_helper import LexerTestCase

class TestHoot(LexerTestCase):

    def test_hoot(self):
        self.assertTokenTypes(
            'hoot()',
            ('hoot', 'HOOT'),
            ('(', 'LPAREN'),
            (')', 'RPAREN'),
        )