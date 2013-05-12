import unittest
import textwrap

from test.parse_helper import ParserTestCase

class TestParameters(ParserTestCase):
	# Do we need to test a single parameter? same as string
	def test_parameter(self):
		owl = textwrap.dedent(r"""
            int a
            int b
            int c
            int d
            void test() {
            }
			test(a, b, c, d)
		""")
		python = textwrap.dedent(r"""
            a = 0
            b = 0
            c = 0
            d = 0
            def test():
                pass
            test(a, b, c, d)
		""")
		self.assertAST(owl, python)
