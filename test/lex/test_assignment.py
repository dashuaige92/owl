import unittest

from test.lex_helper import LexerTestCase

class TestAssignment(LexerTestCase):

	def test_assign_equal(self):
		self.assertTokenTypes(
			'x = 0',
			('x', 'NAME'),
			('=', 'EQUAL'),
			('0', 'LIT_INT'),
		)
	def test_assign_plus_equal(self):
		self.assertTokenTypes(
			'x += 1',
			('x', 'NAME'),
			('+=', 'PEQUAL'),
			('1', 'LIT_INT'),
		)
	def test_assign_minus_equal(self):
		self.assertTokenTypes(
			'x -= 1',
			('x', 'NAME'),
			('-=', 'MEQUAL'),
			('1', 'LIT_INT'),
		)
	def test_assign_times_equal(self):
		self.assertTokenTypes(
			'x *= 1',
			('x', 'NAME'),
			('*=', 'TEQUAL'),
			('1', 'LIT_INT'),
		)
	def test_assign_div_equal(self):
		self.assertTokenTypes(
			'x /= 1',
			('x', 'NAME'),
			('/=', 'DEQUAL'),
			('1', 'LIT_INT'),
		)