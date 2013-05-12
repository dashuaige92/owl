import unittest
import textwrap

from test.parse_helper import TransformTestCase

class TestFunctionCall(TransformTestCase):
	def test_print_function(self):
		owl = textwrap.dedent(r"""
			print("hello")
			""")
		python = textwrap.dedent(r"""
			print 'hello'
			""")
		self.assertAST(owl, python)

	def test_function_call_without_parameters(self):
		owl = textwrap.dedent(
            r"""
            void test(){
            }
			test()
			""")
		python = textwrap.dedent(
            r"""
def test():
    pass
test()
			""")		
		self.assertAST(owl, python)

	def test_function_call_1(self):
		owl = textwrap.dedent(r"""
            void test(int x){
            }
			test(1)
			""")
		python = textwrap.dedent(r"""
def test(x):
    pass
test(1)
			""")		
		self.assertAST(owl, python)

	def test_function_call_2(self):
		owl = textwrap.dedent(r"""
            void test(int a, int b){
            }
			test(1, 2)
			""")
		python = textwrap.dedent(r"""
def test(a,b):
    pass
test(1, 2)
			""")		
		self.assertAST(owl, python)

	def test_function_call_3(self):
		owl = textwrap.dedent(r"""
            void test(int a, int b, int c){
            }
			test(1, 2, 3)
			""")
		python = textwrap.dedent(r"""
def test(a,b,c):
    pass
test(1, 2, 3)
			""")		
		self.assertAST(owl, python)

	def test_built_in_function_call(self):
		owl = textwrap.dedent(r"""
            machine m = {
                node a
            }
			m.step("1")
			""")
		python = textwrap.dedent(r"""
            a = State()
            m = Automaton([a],[],a)
            m.step("1")
			""")		
		self.assertTransformedAST(owl, python)


	def test_bracket_function(self):
		owl = textwrap.dedent(r"""
			string[] test_list = ["a","b"]
			test_list[1]

			""")
		python = textwrap.dedent(r"""
			test_list = ["a","b"]
			test_list[1]
			""")		
		self.assertAST(owl, python)


