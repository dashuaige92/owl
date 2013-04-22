import unittest
import textwrap

from test.parse_helper import ParserTestCase

class TestFunctionDef(ParserTestCase):

	def test_function_def(self):
		owl = textwrap.dedent(r"""
			string test(string x) {
				print(x)
			}
			""")
		python = textwrap.dedent(r"""
			def test(x):
				print x
			""")
		self.assertAST(owl, python)

		owl = textwrap.dedent(r"""
			string test() {
				print(x)
			}
			""")
		python = textwrap.dedent(r"""
			def test():
				print x
			""")
		self.assertAST(owl, python)