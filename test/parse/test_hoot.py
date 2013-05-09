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
