import unittest
import warnings

from owl.lex import lexer
from owl.errors import LexError

class LexerTestCase(unittest.TestCase):
    """A test case that includes helper assertion methods for Owl's lexer.
    """
    def assertTokens(self, string, *tokens):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')

            lexer.input(string)
            toks = tuple((tok.value, tok.type) for tok in lexer)

            lex_warnings = len([l for l in w if issubclass(l.category, LexError)])
            if lex_warnings != 0:
                raise AssertionError('Unexpected LexError!')

        if toks != tokens:
            raise AssertionError(str(toks) + ' != ' + str(tokens))

    def assertTokenTypes(self, string, *tokens):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')

            lexer.input(string)
            toks = tuple((tok.value, tok.type) for tok in lexer)

            lex_warnings = len([l for l in w if issubclass(l.category, LexError)])
            if lex_warnings != 0:
                raise AssertionError('Unexpected LexError!')

        if toks != tokens:
            w = max(len(str(tok)) for tok in toks)
            raise AssertionError(
                'Token types not equal.\n' +
                '\n'.join(
                    ('{:%d} {:%d}' % (w, w)).format(str(t[0]), str(t[1]))
                    for t in zip(('Lexed:',) + toks, ('Expected:',) + tokens)
                )
            )

    def assertLexError(self, string, error_count=1):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')

            lexer.input(string)

            # We need to lex the whole string to get any errors
            [tok for tok in lexer]

            lex_warnings = len([l for l in w if issubclass(l.category, LexError)])
            if lex_warnings != error_count:
                raise AssertionError(
                    'Expected %d lex errors. Got %d.' % (error_count, lex_warnings)
                )
