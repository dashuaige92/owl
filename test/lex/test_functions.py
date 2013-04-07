import unittest

from test.lex_helper import LexerTestCase

class TestFunctionCall(LexerTestCase):
	def test_basic_function(self):
		self.assertTokens(
			'test("test")',
			'test',
			'(',
			'"test"',
			')',
		)
	def test_dot_operator(self):
		self.assertTokens(
			'test.test_function',
			'test',
			'.',
			'test_function',
		)
	def test_built_in_functions(self):
		self.assertTokens(
			'machine.run(3)',
			'machine',
			'.',
			'run',
			'(',
			'3',
			')',
		)
	def test_bracket_function(self):
		self.assertTokens(
			'list[0]',
			'list',
			'[',
			'0',
			']',
		)
	def test_print_function(self):
		self.assertTokens(
			'print("hello there")',
			'print',
			'(',
			'"hello there"',
			')',
		)
		

