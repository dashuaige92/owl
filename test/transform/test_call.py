import unittest
import textwrap

from test.parse_helper import TransformTestCase

class TestCall(TransformTestCase):
	def test_call_typecasting_valid(self):
		owl = textwrap.dedent(r"""
			int i = 0
			toString(i)
			""")
		self.assertNoTransformError(owl)

	def test_call_simple_valid(self):
		owl = textwrap.dedent(r"""
			int func() {
				return 1
			}
			func()
			""")
		self.assertNoTransformError(owl)

	# Invalid
	def test_call_typecasting_invalid(self):
		owl = textwrap.dedent(r"""
			int[] i = [0, 1, 2]
			toString(i)
			""")
		self.assertTransformError(owl)

	def test_call_simple_invalid(self):
		owl = textwrap.dedent(r"""
			int func(int x) {
				return 1
			}
			string x = "hello"
			func(x)
			""")
		self.assertTransformError(owl)
	def test_call_simple2_invalid(self):
		owl = textwrap.dedent(r"""
			int func(int x, string y, bool z) {
				return 1
			}
			int a = 0
			string b = "1"
			bool c = true
			func(c, b, a)
			""")
		self.assertTransformError(owl)
	def test_call_step_empty_invalid(self):
		owl = textwrap.dedent(r"""
			machine m = {
				node s0
			}
			m.step()
			""")
		self.assertTransformError(owl)
	def test_call_step_mult_invalid(self):
		owl = textwrap.dedent(r"""
			machine m = {
				node s0
			}
			m.step("hi", "bye")
			""")
		self.assertTransformError(owl)
