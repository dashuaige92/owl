import unittest
import textwrap

from test.parse_helper import TransformTestCase

class TestList(TransformTestCase):
	def test_list_floats_valid(self):
		owl = textwrap.dedent(r"""
			float[] f = [1, 2, 3, 4, 5]
			""")
		self.assertNoTransformError(owl)
