import unittest

from test.lex_helper import LexerTestCase

class TestUnaryOp(LexerTestCase):

	def test_unary_minux(self):
		self.assertTokenTypes(
			'-1',
			('-', 'MINUS'),
			('1', 'LIT_INT'),
		)
	def test_unary_not(self):
		self.assertTokenTypes(
			'not True',
			('not', 'NOT'),
			('True', 'TRUE'),
		)