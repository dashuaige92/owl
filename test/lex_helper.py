import unittest

from owl.lex import lexer

class LexerTestCase(unittest.TestCase):
    """A test case that includes helper assertion methods for Owl's lexer.
    """
    def assertTokens(self, string, *tokens, **kwargs):
        msg = kwargs.get('msg')
        lexer.input(string)
        toks = tuple(map(lambda t: t.value, [tok for tok in lexer]))
        if toks != tokens:
            raise AssertionError(str(toks) + ' != ' + str(tokens))
