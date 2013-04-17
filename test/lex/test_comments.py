import unittest

from test.lex_helper import LexerTestCase

class TestComments(LexerTestCase):
	def test_basic_comment(self):
		self.assertTokenTypes(
		'# Hi there guys!',
		)
	def test_code_comment(self):
		self.assertTokenTypes(
		'int c # Hi there guys!',
		('int', 'INT'),
		('c', 'NAME'),
		)
	def test_code_comment(self):
		self.assertTokenTypes(
		r"""int c # Hi there line 1
		# Hi there line 2
		""",
		('int', 'INT'),
		('c', 'NAME'),
		('\n', 'NEWLINE'),
		('\n', 'NEWLINE'),
		)
