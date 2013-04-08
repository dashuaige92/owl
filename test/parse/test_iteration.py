import unittest
import textwrap

from test.parse_helper import ParserTestCase

class TestIteration(ParserTestCase):

    def test_for(self):
        owl = textwrap.dedent(r"""
        for x in l {
            print("Hello")
        }
        """)
        python = textwrap.dedent(r"""
        for x in l:
            print 'Hello'
        """)
        self.assertAST(owl, python)

    def test_while(self):
        owl = textwrap.dedent(r"""
        while(x) {
            print("Hello")
        }
        """)
        python = textwrap.dedent(r"""
        while x:
            print 'Hello'
        """)
        self.assertAST(owl, python)
