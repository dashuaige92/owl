import unittest
import textwrap

from test.parse_helper import ParserTestCase

class TestInput(ParserTestCase):
	def test_input(self):
		owl = textwrap.dedent(r"""
		hoot()
		""")
		python = textwrap.dedent(r"""
		print '\a'
		""")
		self.assertAST(owl, python)
