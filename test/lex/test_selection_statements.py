import unittest

from test.lex_helper import LexerTestCase

class TestSelectionStatements(LexerTestCase):

    def test_if_statement(self):
        self.assertTokenTypes(
            'if(True) {\n}',
            ('if', 'IF'),
            ('(', 'LPAREN'),
            ('True', 'TRUE'),
            (')', 'RPAREN'),
            ('{', 'LBRACE'),
            ('\n', 'NEWLINE'),
            ('}', 'RBRACE'),
        )

    def test_if_else_statement(self):
        self.assertTokenTypes(
            'if(True) {\n} else {\n}',
            ('if', 'IF'),
            ('(', 'LPAREN'),
            ('True', 'TRUE'),
            (')', 'RPAREN'),
            ('{', 'LBRACE'),
            ('\n', 'NEWLINE'),
            ('}', 'RBRACE'),
            ('else', 'ELSE'),
            ('{', 'LBRACE'),
            ('\n', 'NEWLINE'),
            ('}', 'RBRACE'),
        )