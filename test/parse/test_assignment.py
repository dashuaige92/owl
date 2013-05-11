import unittest
import textwrap

from test.parse_helper import ParserTestCase

class TestAssignment(ParserTestCase):

	def test_assign_equal(self):
		owl = textwrap.dedent(
			r"""
			x = 0
			""")
		python = textwrap.dedent(
			r"""
			x = 0
			""")
		self.assertAST(owl, python)
	def test_assign_list_equal(self):
		owl = textwrap.dedent(
			r"""
			l[0] = 0
			""")
		python = textwrap.dedent(
			r"""
			l[0] = 0
			""")
		self.assertAST(owl, python)
	def test_assign_plus_equal(self):
		owl = textwrap.dedent(
			r"""
			x += 1
			""")
		python = textwrap.dedent(
			r"""
			x += 1
			""")
		self.assertAST(owl, python)
	def test_assign_minus_equal(self):
		owl = textwrap.dedent(
			r"""
			x -= 1
			""")
		python = textwrap.dedent(
			r"""
			x -= 1
			""")
		self.assertAST(owl, python)
	def test_assign_times_equal(self):
		owl = textwrap.dedent(
			r"""
			x *= 1
			""")
		python = textwrap.dedent(
			r"""
			x *= 1
			""")
		self.assertAST(owl, python)
	def test_assign_div_equal(self):
		owl = textwrap.dedent(
			r"""
			x /= 1
			""")
		python = textwrap.dedent(
			r"""
			x /= 1
			""")
		self.assertAST(owl, python)