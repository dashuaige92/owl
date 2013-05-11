import unittest
import textwrap

from test.lex_helper import LexerTestCase

class TestLists(LexerTestCase):
    def test_lists(self):
        self.assertTokenTypes(
            'machine m = { node a \n node b \n enter(a) { \n } \n a("1") -> b { \n }',
            ('machine', 'MACHINE'),
            ('m', 'NAME'),
            ('=', 'EQUAL'),
            ('{', 'LBRACE'),
            ('node', 'NODE'),
            ('a', 'NAME'),
            ('\n', 'NEWLINE'),
            ('node', 'NODE'),
            ('b', 'NAME'),
            ('\n', 'NEWLINE'),
            ('enter', 'ENTER'),
            ('(', 'LPAREN'),
            ('a', 'NAME'),
            (')', 'RPAREN'),
            ('{', 'LBRACE'),
            ('\n', 'NEWLINE'),
            ('}', 'RBRACE'),
            ('\n', 'NEWLINE'),
            ('a', 'NAME'),
            ('(', 'LPAREN'),
            ('"1"', 'LIT_STRING'),
            (')', 'RPAREN'),
            ('->', 'ARROW'),
            ('b', 'NAME'),
            ('{', 'LBRACE'),
            ('\n', 'NEWLINE'),
            ('}', 'RBRACE'),
        )