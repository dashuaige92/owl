import unittest
import textwrap

from test.parse_helper import ParserTestCase

class TestIteration(ParserTestCase):

    def test_for_loop(self):
        owl = textwrap.dedent(
            r"""
            int x
            int[] l
            for x in l {
                print("Hello")
            }
            """)
        python = textwrap.dedent(
            r"""
            x = 0
            l = []
            for x in l:
                print 'Hello'
            """)
        self.assertAST(owl, python)

    def test_for_loop_on_uninitialized_variable_raises_error(self):
        owl = textwrap.dedent(
            r"""
            int[] l
            for x in l {
                print("Hello")
            }
            """)
        self.assertParseError(owl)

    def test_while(self):
        owl = textwrap.dedent(
            r"""
            bool x
            while(x) {
                print("Hello")
            }
            """)
        python = textwrap.dedent(
            r"""
            x = False
            while x:
                print 'Hello'
            """)
        self.assertAST(owl, python)
