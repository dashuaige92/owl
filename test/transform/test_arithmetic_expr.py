import unittest
import textwrap

from test.parse_helper import TransformTestCase

class TestArithmeticExpr(TransformTestCase):
	def test_addition_valid(self):
		owl = textwrap.dedent(r"""
			5 + 10
			""")
		self.assertNoTransformError(owl)
