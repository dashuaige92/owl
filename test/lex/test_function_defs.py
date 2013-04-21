import unittest

from test.lex_helper import LexerTestCase

class TestFunctionDef(LexerTestCase):

	def test_function_def(self):
		self.assertTokenTypes(
			'int test(int x) {\n}',
			('int', 'INT'),
			('test', 'NAME'),
			('(', 'LPAREN'),
			('int', 'INT'),
			('x', 'NAME'),
			(')', 'RPAREN'),
            ('{', 'LBRACE'),
            ('\n', 'NEWLINE'),
            ('}', 'RBRACE'),
		)

	def test_function_def_noparam(self):
		self.assertTokenTypes(
			'int test() {\n}',
			('int', 'INT'),
			('test', 'NAME'),
			('(', 'LPAREN'),
			(')', 'RPAREN'),
            ('{', 'LBRACE'),
            ('\n', 'NEWLINE'),
            ('}', 'RBRACE'),
		)

	def test_function_def_void(self):
		self.assertTokenTypes(
			'void test() {\n}',
			('void', 'VOID'),
			('test', 'NAME'),
			('(', 'LPAREN'),
			(')', 'RPAREN'),
            ('{', 'LBRACE'),
            ('\n', 'NEWLINE'),
            ('}', 'RBRACE'),
		)