import unittest
import textwrap

from test.parse_helper import ParserTestCase

class TestUnaryOp(ParserTestCase):

	def test_toInt(self):
		owl = textwrap.dedent(
			r"""
            toInt("1" + "2")
			""")
		python = textwrap.dedent(
			r"""
            int('1' + '2')
			""")
		self.assertAST(owl, python)

	def test_toBool(self):
		owl = textwrap.dedent(
			r"""
            toBool(1)
			""")
		python = textwrap.dedent(
			r"""
            bool(1)
			""")
		self.assertAST(owl, python)

	def test_toFloat(self):
		owl = textwrap.dedent(
			r"""
            toFloat("1." + "2")
			""")
		python = textwrap.dedent(
			r"""
            float('1.' + '2')
			""")
		self.assertAST(owl, python)

	def test_toString(self):
		owl = textwrap.dedent(
			r"""
            toString(12)
			""")
		python = textwrap.dedent(
			r"""
            str(12)
			""")
		self.assertAST(owl, python)
