import unittest
import textwrap

from test.parse_helper import TransformTestCase

class TestAssign(TransformTestCase):
	def test_simple_assign_valid(self):
		owl = textwrap.dedent(r"""
			string s = "hello"
			""")
		python = textwrap.dedent(r"""
			s = 'hello'
			""")
		self.assertTransformedAST(owl, python)

	def test_simple_assign_invalid(self):
		owl = textwrap.dedent(r"""
			string s = 5
			""")
		self.assertTransformError(owl)