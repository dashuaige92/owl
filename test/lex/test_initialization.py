import unittest

from test.lex_helper import LexerTestCase

class TestInitialization(LexerTestCase):
	def test_declare(self):
		self.assertTokens(
			'machine m',
			'machine',
			'm',
			)
	def test_declare_init(self):
		self.assertTokens(
			'string s = "test"',
			'string',
			's',
			'=',
			'"test"',
			)
	#test default init