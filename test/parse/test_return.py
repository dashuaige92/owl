import unittest
import textwrap

from test.parse_helper import ParserTestCase

class TestReturn(ParserTestCase):
	def test_return_simple(self):
		owl = textwrap.dedent(r"""
		void foo(){
			return
		}
		""")
		python = textwrap.dedent(r"""
		def foo():
			return
		""")
		self.assertAST(owl, python)
