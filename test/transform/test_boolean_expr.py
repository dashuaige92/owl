import unittest
import textwrap

from test.parse_helper import TransformTestCase

class TestBooleanExpr(TransformTestCase):
	def test_bool_simple_valid(self):
		owl = textwrap.dedent(r"""
			True or False
			""")
		self.assertNoTransformError(owl)
	def test_bool_valid(self):
		owl = textwrap.dedent(r"""
			bool t = True
			t and False
			""")
		self.assertNoTransformError(owl)
	def test_bool_mult_and_valid(self):
		owl = textwrap.dedent(r"""
			bool t = True
			t and False and True and False 
			""")
		self.assertNoTransformError(owl)
	def test_bool_mult_or_valid(self):
		owl = textwrap.dedent(r"""
			bool t = True
			t or False or True or False 
			""")
		self.assertNoTransformError(owl)
	def test_bool_mix_valid(self):
		owl = textwrap.dedent(r"""
			bool t = True
			t or False and True and False 
			""")
		self.assertNoTransformError(owl)

	# Invalid
	def test_bool_simple_invalid(self):
		owl = textwrap.dedent(r"""
			True or "False"
			""")
		self.assertTransformError(owl)
	def test_bool_var_invalid(self):
		owl = textwrap.dedent(r"""
			string s = "True"
			True or s
			""")
		self.assertTransformError(owl)



