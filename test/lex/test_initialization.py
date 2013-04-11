import unittest

from test.lex_helper import LexerTestCase

class TestInitialization(LexerTestCase):

    def test_declare(self):
        self.assertTokenTypes(
            'string s',
            ('string', 'STRING'),
            ('s', 'NAME'),
        )

    def test_declare_init(self):
        self.assertTokenTypes(
            'string s = "test"',
            ('string', 'STRING'),
            ('s', 'NAME'),
            ('=', 'EQUAL'),
            ('"test"', 'LIT_STRING'),
        )
