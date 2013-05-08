import unittest
import textwrap

from test.parse_helper import ParserTestCase

class TestInput(ParserTestCase):
	def test_input(self):
		owl = textwrap.dedent(r"""
		string x = input("Enter: ")
		""")
		python = textwrap.dedent(r"""
		x = raw_input("Enter: ")
		""")
		self.assertAST(owl, python)
