import unittest
import textwrap

from test.parse_helper import TransformTestCase

class TestUnaryExpr(TransformTestCase):
	def test_unary_minus_valid(self):
		owl = textwrap.dedent(r"""
			-5
			""")
		self.assertNoTransformError(owl)
	def test_unary_minus_int_valid(self):
		owl = textwrap.dedent(r"""
			int a = 5
			-a
			""")
		self.assertNoTransformError(owl)
	def test_unary_minus_float_valid(self):
		owl = textwrap.dedent(r"""
			float a = 5.5
			-a
			""")
		self.assertNoTransformError(owl)
	def test_unary_not_bool_valid(self):
		owl = textwrap.dedent(r"""
			string T = "true"
			not True
			""")
		self.assertNoTransformError(owl)


	# Invalid
	def test_unary_minus_invalid(self):
		owl = textwrap.dedent(r"""
			string s = "5.5"
			-s
			""")
		self.assertTransformError(owl)
	
	def test_unary_not_bool_invalid(self):
		owl = textwrap.dedent(r"""
			string s = "true"
			not s
			""")
		self.assertTransformError(owl)
		# This should not work, needs to convert to _True
	# def test_unary_not_bool2_invalid(self):
	# 	owl = textwrap.dedent(r"""
	# 		string True = "true"
	# 		not True
	# 		""")
	# 	self.assertTransformError(owl)

