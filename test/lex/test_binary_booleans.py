import unittest

from test.lex_helper import LexerTestCase

class TestBinaryBooleans(LexerTestCase):

	def test_and_op(self):
		self.assertTokenTypes(
			'a and b',
			 ('a', 'NAME'),
			 ('and', 'AND'),
			 ('b', 'NAME'),
		)
	def test_or_op(self):
		self.assertTokenTypes(
			'a or b',
			 ('a', 'NAME'),
			 ('or', 'OR'),
			 ('b', 'NAME'),
		)