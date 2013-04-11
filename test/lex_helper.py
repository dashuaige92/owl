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

    def assertTokenTypes(self, string, *tokens, **kwargs):
        msg = kwargs.get('msg')
        lexer.input(string)
        toks = tuple((tok.value, tok.type) for tok in lexer)
        if toks != tokens:
            w = max(len(str(tok)) for tok in toks)
            raise AssertionError(
                'Token types not equal.\n' +
                '\n'.join(
                    ('{:%d} {:%d}' % (w, w)).format(str(t[0]), str(t[1]))
                    for t in zip(('Lexed:',) + toks, ('Expected:',) + tokens)
                )
            )
