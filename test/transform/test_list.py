import unittest
import textwrap

from test.parse_helper import TransformTestCase

class TestList(TransformTestCase):
	def test_list_floats_valid(self):
		owl = textwrap.dedent(r"""
			float[] f = [1, 2, 3, 4, 5]
			""")
		self.assertNoTransformError(owl)
	def test_list_bool_valid(self):
		owl = textwrap.dedent(r"""
			bool[] b = [true, false, true]
			""")
		self.assertNoTransformError(owl)

	# Invalid
	def test_list_int_invalid(self):
		owl = textwrap.dedent(r"""
			int[] i = [1, 2, 3, 4, 5.5]
			""")
		self.assertTransformError(owl)
	def test_list_str_invalid(self):
		owl = textwrap.dedent(r"""
			string[] s = ["1", "2", true]
			""")
		self.assertTransformError(owl)
	def test_list_bool_invalid(self):
		owl = textwrap.dedent(r"""
			bool[] b = [true, false, 1]
			""")
		self.assertTransformError(owl)
	def test_list_list_invalid(self):
		owl = textwrap.dedent(r"""
			int[] i = [1]
			int[] j = [1, 2, 3, i]
			""")
		self.assertTransformError(owl)
