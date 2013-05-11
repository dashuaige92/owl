import unittest
import textwrap

from test.parse_helper import TransformTestCase

class TestSubscript(TransformTestCase):
	def test_list_indexing_valid(self):
		owl = textwrap.dedent(r"""
			bool[] b = [True, False]
			b[0]
			""")
		self.assertNoTransformError(owl)
	def test_list_indexing_var_valid(self):
		owl = textwrap.dedent(r"""
			bool[] b = [True, False]
			int i = 0
			b[i]
			""")
		self.assertNoTransformError(owl)

	# Invalid
	def test_list_indexing_invalid(self):
		owl = textwrap.dedent(r"""
			bool[] b = [True, False]
			float f = 1
			b[f]
			""")
		self.assertTransformError(owl)