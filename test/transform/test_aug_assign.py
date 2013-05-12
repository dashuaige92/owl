import unittest
import textwrap

from test.parse_helper import TransformTestCase

class TestAugAssign(TransformTestCase):
	def test_aug_assign_plus_float_valid(self):
		owl = textwrap.dedent(r"""
			float i = 0
			i += 10
			""")
		self.assertNoTransformError(owl)
	def test_aug_assign_plus_string_valid(self):
		owl = textwrap.dedent(r"""
			string s = "hi"
			s += " there"
			""")
		self.assertNoTransformError(owl)
	def test_aug_assign_string2_valid(self):
		owl = textwrap.dedent(r"""
			string s = "Hi"
			s += toString(10)
			""")
		self.assertNoTransformError(owl)
	def test_aug_assign_int_valid(self):
		owl = textwrap.dedent(r"""
			float i = 0
			i += 10
			""")
		self.assertNoTransformError(owl)
	
	# Invalid
	def test_aug_assign_plus_invalid(self):
		owl = textwrap.dedent(r"""
			float i = 0
			i += "10"
			""")
		self.assertTransformError(owl)
	def test_aug_assign_str_invalid(self):
		owl = textwrap.dedent(r"""
			string s = "Hi"
			s -= " there!"
			""")
		self.assertTransformError(owl)
	def test_aug_assign_str2_invalid(self):
		owl = textwrap.dedent(r"""
			string s = "Hi"
			s *= " there!"
			""")
		self.assertTransformError(owl)
	def test_aug_assign_str3_invalid(self):
		owl = textwrap.dedent(r"""
			string s = "Hi"
			s /= " there!"
			""")
		self.assertTransformError(owl)
	def test_aug_assign_str4_invalid(self):
		owl = textwrap.dedent(r"""
			string s = "Hi"
			s += 10
			""")
		self.assertTransformError(owl)