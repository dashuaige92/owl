import unittest
import textwrap

from test.parse_helper import ParserTestCase

class TestHoot(ParserTestCase):
	def test_hoot(self):
		owl = textwrap.dedent(r"""
		hoot()
		""")
		python = textwrap.dedent(r"""
		print '\a'
		""")
		self.assertAST(owl, python)

	def test_hoot_with_argument_raises_error(self):
		owl = textwrap.dedent(r"""
		hoot("hi")
		""")
		self.assertParseError(owl)