import unittest
import textwrap

from test.parse_helper import TransformTestCase

class TestInput(TransformTestCase):
	def test_input(self):
		owl = textwrap.dedent(r"""
			string x = input("Enter: ")
			""")
		self.assertNoTransformError(owl)
