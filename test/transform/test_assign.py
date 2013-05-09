import unittest
import textwrap

from test.parse_helper import TransformTestCase

class TestInitialization(TransformTestCase):
	def test_str_assign_valid(self):
		owl = textwrap.dedent(r"""
				string s = "hello"
				s = "hi"
				""")
		python = textwrap.dedent(r"""
				s = 'hello'
				s = 'hi'
				""")
		self.assertTransformedAST(owl, python)
	def test_list_assign_valid(self):
		owl = textwrap.dedent(r"""
				int[] l = []
				l = [1, 2, 3]
				""")
		python = textwrap.dedent(r"""
				l = []
				l = [1, 2, 3]
				""")

	# Invalid Tests
	def test_str_assign_invalid(self):
		owl = textwrap.dedent(r"""
			string s
			s = 5
			""")
		self.assertTransformError(owl)
	def test_int_assign_invalid(self):
		owl = textwrap.dedent(r"""
			int i
			i = 5.5
			""")
		self.assertTransformError(owl)

	# Not Working
	def test_float_assign_invalid(self):
		owl = textwrap.dedent(r"""
			float f
			f = 100.5
			""")
		self.assertTransformError(owl)

	def test_list_assign_invalid(self):
		owl = textwrap.dedent(r"""
				int[] num_list
				num_list = [1, "2", "3"]
				""")
		self.assertTransformError(owl)

