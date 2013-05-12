import unittest
import textwrap

from test.parse_helper import TransformTestCase

class TestFor(TransformTestCase):
	def test_for_list_range(self):
		owl = textwrap.dedent(r"""
			int i
			for i in range(1, 10) {
				print(i)
			}
			""")
		self.assertNoTransformError(owl)

	def test_for_int_in_int_list(self):
		owl = textwrap.dedent(r"""
			int i
			int[] list = [1, 2, 3]
			for i in list {
				print(i)
			}
			""")
		self.assertNoTransformError(owl)

	def test_for_float_in_float_list(self):
		owl = textwrap.dedent(r"""
			float f
			float[] list = [1, 2, 3, 4, 5.5]
			for f in list {
				print(f)
			}
			""")
		self.assertNoTransformError(owl)

	# Invalid
	def test_for_int_in_float_list_invalid(self):
		owl = textwrap.dedent(r"""
			int i
			float[] list = [1, 2, 3, 4, 5.5]
			for i in list {
				print(i)
			}
			""")
		self.assertTransformError(owl)
