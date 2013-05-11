import unittest
import textwrap

from test.parse_helper import TransformTestCase

class TestSubscript(TransformTestCase):
	def test_list_indexing_valid(self):
		owl = textwrap.dedent(r"""
			bool[] b = [true, false]
			b[0]
			""")
		self.assertNoTransformError(owl)
	def test_list_indexing_var_valid(self):
		owl = textwrap.dedent(r"""
			bool[] b = [true, false]
			int i = 0
			b[i]
			""")
		self.assertNoTransformError(owl)

	# Invalid
	def test_list_indexing_invalid(self):
		owl = textwrap.dedent(r"""
			bool[] b = [true, false]
			float f = 1
			b[f]
			""")
		self.assertTransformError(owl)