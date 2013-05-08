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


	def test_function_def_2(self):


		owl = textwrap.dedent(r"""
			string test() {
                print("1")
                print("1")
                print("1")
			}
			""")
		python = textwrap.dedent(r"""
def test():
    print "1"
    print "1"
    print "1"

""")
		self.assertAST(owl, python)