import unittest
import textwrap

from test.parse_helper import TransformTestCase

class TestFunctionDef(TransformTestCase):
	def test_function_def_simple_valid(self):
		owl = textwrap.dedent(r"""
			int func() {
				return 1
			}
			""")
		self.assertNoTransformError(owl)
	def test_function_def_simple_for_valid(self):
		owl = textwrap.dedent(r"""
			int func() {
				int i
				int[] list = [1, 2, 3, 4, 5]
				for i in list {
					return 1
					if (i < 10) {
						return 2
					} else {
						return 3
					}
				}
				return 1
			}""")
		self.assertNoTransformError(owl)
	def test_function_def_simple_void_valid(self):
		owl = textwrap.dedent(r"""
			void func() {
				return
			}
			""")
		self.assertNoTransformError(owl)
	
	def test_function_def_nested_if_valid(self):
		owl = textwrap.dedent(r"""
			int func() {
				int x = 0
				if (x == 0) {
					return 0
				} else {
					return 1
				}
				return x
			}
			""")
		self.assertNoTransformError(owl)
	def test_function_def_nested_while_valid(self):
		owl = textwrap.dedent(r"""
			int func(int x, int y) {
				if (x == 0) {
					return 0
				} else {
					while (x) {
						return x
					}
				}
				return x
			}
			""")
		self.assertNoTransformError(owl)


	# Invalid 
	def test_function_def_simple_invalid(self):
		owl = textwrap.dedent(r"""
			int func() {
				return "1"
			}
			""")
		self.assertTransformError(owl)
	def test_function_def_mult_returns_invalid(self):
		owl = textwrap.dedent(r"""
			int func() {
				return 1
				return "hello"
			}
			""")
		self.assertTransformError(owl)

	def test_function_def_for_invalid(self):
		owl = textwrap.dedent(r"""
			string func() {
				int i
				int[] list = [1, 2, 3, 4, 5]
				for i in list {
					return "1"
					if (i < 10) {
						return "2"
					} else {
						return "3"
					}
					return 8
				}
			}""")
		self.assertTransformError(owl)
	def test_function_def_nested_while_invalid(self):
		owl = textwrap.dedent(r"""
			int func() {
				int x = 0
				if (x == 0) {
					return 0
				} else {
					while (x) {
						return "x"
					}
				}
				return x
			}
			""")
		self.assertTransformError(owl)
	def test_function_def_nested_while2_invalid(self):
		owl = textwrap.dedent(r"""
			int func() {
				int x = 0
				if (x == 0) {
					return 0
				} else {
					while (x) {
						if (x == 1) {
							return x
						} else {
							return x*5.5
						}
					}
				}
				return x
			}
			""")
		self.assertTransformError(owl)

	def test_function_def_params_invalid(self):
		owl = textwrap.dedent(r"""
			int func(int x, float y) {
				if (x == 0) {
					return 0
				} else {
					while (x) {
						return y
					}
				}
				return x
			}
			""")
		self.assertTransformError(owl)
