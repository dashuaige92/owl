import unittest
import textwrap

from test.parse_helper import ParserTestCase

class TestLiterals(ParserTestCase):
    def test_string_literal(self):
        owl = textwrap.dedent(r"""
        print("Hello, world!")
        """)
        python = textwrap.dedent(r"""
        print 'Hello, world!'
        """)
        self.assertAST(owl, python)

    def test_int_literal(self):
        owl = textwrap.dedent(r"""
        print(3)
        """)
        python = textwrap.dedent(r"""
        print 3
        """)
        self.assertAST(owl, python)
