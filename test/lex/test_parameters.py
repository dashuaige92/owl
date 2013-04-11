import unittest

from test.lex_helper import LexerTestCase

class TestParameters(LexerTestCase):
	def test_parameter(self):
		self.assertTokenTypes(
			'a',
			 ('a', 'NAME'),
		)	
	def test_parameter_list(self):
		self.assertTokenTypes(
			'a, b, c, d',
			('a', 'NAME'),
			(',', 'COMMA'),
			('b', 'NAME'),
			(',', 'COMMA'),
			('c', 'NAME'),
			(',', 'COMMA'),
			('d', 'NAME'),
		)