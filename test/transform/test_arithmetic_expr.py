import unittest
import textwrap

from test.parse_helper import TransformTestCase

class TestArithmeticExpr(TransformTestCase):
	def test_addition_valid(self):
		owl = textwrap.dedent(r"""
			5 + 10
			""")
		self.assertNoTransformError(owl)
	def test_addition_valid_2(self):
		owl = textwrap.dedent(r"""
			int i = 10
			i + 10
			""")
		self.assertNoTransformError(owl)

	def test_addition_valid_3(self):
		owl = textwrap.dedent(r"""
			int i = 10
			i + 10 + 100
			""")
		self.assertNoTransformError(owl)



	# Invalid
	def test_addition_invalid(self):
		owl = textwrap.dedent(r"""
			5 + "10hello"
			""")
		self.assertTransformError(owl)

	def test_addition_invalid_2(self):
		owl = textwrap.dedent(r"""
			5 + "100" + 5
			""")
		self.assertTransformError(owl)

	def test_addition_invalid_3(self):
		owl = textwrap.dedent(r"""
			5 + "100" + "hello"
			""")
		self.assertTransformError(owl)
	def test_addition_invalid_3(self):
		owl = textwrap.dedent(r"""
			void func() {
				return
			}
			5 + "100" + func()
			""")
		self.assertTransformError(owl)


	# Test op with function call
