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



	def test_list_init_invalid(self):
		owl = textwrap.dedent(r"""
				int[] l = [1, "2", "3"]
				""")
		self.assertTransformError(owl)

	def test_str_init_invalid(self):
		owl = textwrap.dedent(r"""
			string s = 5
			""")
		self.assertTransformError(owl)


	def test_str_init_valid1(self):
		owl = textwrap.dedent(r"""
			string s = "hello there"
			int a = 0
			""")
		
		self.assertNoTransformError(owl)
