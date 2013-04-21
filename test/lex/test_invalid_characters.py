import unittest

from test.lex_helper import LexerTestCase

class TestInvalidCharacters(LexerTestCase):

    def test_invalid_tilde(self):
        self.assertLexError("~")

    def test_invalid_backtick(self):
        self.assertLexError("`")

    def test_invalid_exclamation_mark(self):
        self.assertLexError("!")

    def test_invalid_at_sign(self):
        self.assertLexError("@")

    def test_invalid_dollar_sign(self):
        self.assertLexError("$")

    def test_invalid_carat(self):
        self.assertLexError("^")

    def test_invalid_ampersand(self):
        self.assertLexError("&")
