import unittest
import textwrap

from test.parse_helper import TransformTestCase

class TestComparisonExpr(TransformTestCase):
	def test_equal_num_valid(self):
		owl = textwrap.dedent(r"""
			5 == 10
			""")
		self.assertNoTransformError(owl)
	def test_equal_num2_valid(self):
		owl = textwrap.dedent(r"""
			float f = 10.5
			5 == f
			""")
		self.assertNoTransformError(owl)
	def test_equal_str_valid(self):
		owl = textwrap.dedent(r"""
			"5" == "10"
			""")
		self.assertNoTransformError(owl)

	def test_equal_str2_valid(self):
		owl = textwrap.dedent(r"""
			string s = "hi"
			s == "hi"
			""")
		self.assertNoTransformError(owl)


	# Invalid
	def test_equal_num_invalid(self):
		owl = textwrap.dedent(r"""
			5 == "10"
			""")
		self.assertTransformError(owl)
	def test_equal_str_invalid(self):
		owl = textwrap.dedent(r"""
			"5" == 1
			""")
		self.assertTransformError(owl)
	def test_params_invalid(self):
		owl = textwrap.dedent(r"""
			5 == 5 > 5
			""")
		self.assertTransformError(owl)

