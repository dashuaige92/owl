import unittest
import textwrap

from test.parse_helper import TransformTestCase

class TestCall(TransformTestCase):
	def test_call_typecasting_valid(self):
		owl = textwrap.dedent(r"""
			int i = 0
			tostring(i)
			""")
		self.assertNoTransformError(owl)

	# Invalid
	def test_call_typecasting_invalid(self):
		owl = textwrap.dedent(r"""
			int[] i = [0, 1, 2]
			toString(i)
			""")
		self.assertTransformError(owl)
