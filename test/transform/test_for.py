import unittest
import textwrap

from test.parse_helper import TransformTestCase

class TestFor(TransformTestCase):

	@unittest.skip("For list range")	
	def test_for_list_range(self):
		owl = textwrap.dedent(r"""
			int i
			for i in range(1, 10) {
				print(i)
			}
			""")
		self.assertNoTransformError(owl)

	def test_for_list_valid(self):
		owl = textwrap.dedent(r"""
			int i
			int[] list = [1, 2, 3]
			for i in list {
				print(i)
			}
			""")
		self.assertNoTransformError(owl)


	# Invalid
	def test_for_list_type_invalid(self):
		owl = textwrap.dedent(r"""
			int i
			float[] list = [1, 2, 3, 4, 5.5]
			for i in list1 {
				return 0
			}
			""")
		self.assertTransformError(owl)
