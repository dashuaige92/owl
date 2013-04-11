import unittest
import textwrap

from test.parse_helper import ParserTestCase

class TestFunctionCall(ParserTestCase):
	def test_print_function(self):
		owl = textwrap.dedent(r"""
			print("hello")
			""")
		python = textwrap.dedent(r"""
			print 'hello'
			""")
		self.assertAST(owl, python)
	def test_function_call_1(self):
		owl = textwrap.dedent(r"""
			test(1)
			""")
		python = textwrap.dedent(r"""
			test(1)
			""")		
		self.assertAST(owl, python)
	def test_function_call_2(self):
		owl = textwrap.dedent(r"""
			test(1, 2)
			""")
		python = textwrap.dedent(r"""
			test(1, 2)
			""")		
		self.assertAST(owl, python)
	def test_function_call_3(self):
		owl = textwrap.dedent(r"""
			test(1, 2, 3)
			""")
		python = textwrap.dedent(r"""
			test(1, 2, 3)
			""")		
		self.assertAST(owl, python)
