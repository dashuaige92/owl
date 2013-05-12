import unittest
import textwrap

from test.parse_helper import ParserTestCase

class TestUnaryOp(ParserTestCase):

	def test_unary_minus(self):
		owl = textwrap.dedent(
			r"""
            int a
			-a
			""")
		python = textwrap.dedent(
			r"""
a = 0
-a
			""")
		self.assertAST(owl, python)

	def test_unary_negation(self):
		owl = textwrap.dedent(
			r"""
			not True
			""")
		python = textwrap.dedent(
			r"""
			not True
			""")
		self.assertAST(owl, python)