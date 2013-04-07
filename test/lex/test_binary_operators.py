import unittest

from test.lex_helper import LexerTestCase

class test_binary_operators(LexerTestCase):
	def test_plus(self):
		self.assertTokens(
			'1+2',
			'1',
			'+',
			'2',
			)
	def test_minus(self):
		self.assertTokens(
			'2-1',
			'2',
			'-',
			'1',
			)
	def test_times(self):
		self.assertTokens(
			'1*2',
			'1',
			'*',
			'2',
			)
	def test_divide(self):
		self.assertTokens(
			'2/1',
			'2',
			'/',
			'1',
			)