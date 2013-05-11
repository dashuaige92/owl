import unittest
import textwrap

from test.parse_helper import TransformTestCase

class TestInitialization(TransformTestCase):
	def test_str_init_valid(self):
		owl = textwrap.dedent(r"""
			string s = "hello"
			""")
		python = textwrap.dedent(r"""
			s = 'hello'
			""")
		self.assertTransformedAST(owl, python)
	def test_list_int_valid(self):
		owl = textwrap.dedent(r"""
			int[] s = [1, 2, 3]
			""")
		self.assertNoTransformError(owl)
	def test_list_int_expr_valid(self):
		owl = textwrap.dedent(r"""
			int i = 5
			int[] s = [1, 2, i+5]
			""")
		self.assertNoTransformError(owl)
	def test_list_str_valid(self):
		owl = textwrap.dedent(r"""
				string[] s = ["hi", "hi", "hi"]
				""")
		self.assertNoTransformError(owl)
	def test_list_str_valid(self):
		owl = textwrap.dedent(r"""
				print(["hi", "hi", "hi"])
				""")
		self.assertNoTransformError(owl)


	def test_list_init_invalid(self):
		owl = textwrap.dedent(r"""
				int[] l = ["1", "2", "3"]
				""")
		self.assertTransformError(owl)

	def test_list_int_invalid(self):
		owl = textwrap.dedent(r"""
				int[] l = [1.5, 2.5, 3.5]
				""")
		self.assertTransformError(owl)


	def test_str_init_invalid(self):
		owl = textwrap.dedent(r"""
			string s = 5
			""")
		self.assertTransformError(owl)
