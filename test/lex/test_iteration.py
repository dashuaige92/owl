import unittest

from test.lex_helper import LexerTestCase

class TestIteration(LexerTestCase):

    def test_while_loop(self):
        self.assertTokenTypes(
            'while(a) {\n}',
            ('while', 'WHILE'),
            ('(', 'LPAREN'),
            ('a', 'NAME'),
            (')', 'RPAREN'),
            ('{', 'LBRACE'),
            ('\n', 'NEWLINE'),
            ('}', 'RBRACE'),
        )

    def test_for_loop(self):
        self.assertTokenTypes(
            'for a in b {\n}',
            ('for', 'FOR'),
            ('a', 'NAME'),
            ('in', 'IN'),
            ('b', 'NAME'),
            ('{', 'LBRACE'),
            ('\n', 'NEWLINE'),
            ('}', 'RBRACE'),
        )
