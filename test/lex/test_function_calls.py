import unittest

from test.lex_helper import LexerTestCase

class TestFunctionCall(LexerTestCase):

	def test_basic_function(self):
		self.assertTokenTypes(
			'test("test")',
			('test', 'NAME'),
			('(', 'LPAREN'),
			('"test"', 'LIT_STRING'),
			(')', 'RPAREN'),
		)
	
	def test_dot_operator(self):
		self.assertTokenTypes(
			'test.test_function',
			('test', 'NAME'),
			('.', 'DOT'),
			('test_function', 'NAME'),
		)
	
	def test_built_in_functions(self):
		self.assertTokenTypes(
			'machine.run(3)',
			('machine', 'MACHINE'),
			('.', 'DOT'),
			('run', 'NAME'),
			('(', 'LPAREN'),
			('3', 'LIT_NUMBER'),
			(')', 'RPAREN'),
		)
	
	def test_bracket_function(self):
		self.assertTokenTypes(
			'my_list[0]',
			('my_list', 'NAME'),
			('[', 'LBRACK'),
			('0', 'LIT_NUMBER'),
			(']', 'RBRACK'),
		)
	
	def test_print_function(self):
		self.assertTokenTypes(
			'print("hello there")',
			('print', 'PRINT'),
			('(', 'LPAREN'),
			('"hello there"', 'LIT_STRING'),
			(')', 'RPAREN'),
		)