import unittest

from test.lex_helper import LexerTestCase

class TestInvalidCharacters(LexerTestCase):

    def test_invalid_characters(self):
        invalid_characters = "~`!@#$^&"
        self.assertLexError(
            invalid_characters,
            error_count=len(invalid_characters))
