import unittest
import textwrap

from test.parse_helper import TransformTestCase

class TestBooleanExpr(TransformTestCase):
	def test_bool_simple_valid(self):
		owl = textwrap.dedent(r"""
			true or false
			""")
		self.assertNoTransformError(owl)
	def test_bool_valid(self):
		owl = textwrap.dedent(r"""
			bool t = true
			t and false
			""")
		self.assertNoTransformError(owl)
	def test_bool_mult_and_valid(self):
		owl = textwrap.dedent(r"""
			bool t = true
			t and false and true and false 
			""")
		self.assertNoTransformError(owl)
	def test_bool_mult_or_valid(self):
		owl = textwrap.dedent(r"""
			bool t = true
			t or false or true or false 
			""")
		self.assertNoTransformError(owl)
	def test_bool_mix_valid(self):
		owl = textwrap.dedent(r"""
			bool t = true
			t or false and true and false 
			""")
		self.assertNoTransformError(owl)

	# Invalid
	def test_bool_simple_invalid(self):
		owl = textwrap.dedent(r"""
			true or "false"
			""")
		self.assertTransformError(owl)
	def test_bool_var_invalid(self):
		owl = textwrap.dedent(r"""
			string s = "true"
			true or s
			""")
		self.assertTransformError(owl)



