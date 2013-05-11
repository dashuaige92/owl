import unittest
import textwrap

from test.parse_helper import ParserTestCase

class TestBinaryBooleans(ParserTestCase):

    def test_and_op(self):
        owl = textwrap.dedent(
            r"""
            a and b
            """)
        python = textwrap.dedent(
           r"""
           a and b
           """)
        self.assertAST(owl, python)

    def test_or_op(self):
        owl = textwrap.dedent(
            r"""
            a or b
            """)
        python = textwrap.dedent(
        	r"""
        	a or b
            """)
        self.assertAST(owl, python)

    def test_multiple_operators(self):
        owl = textwrap.dedent(
            r"""
            a or (b and c)
            """)
        python = textwrap.dedent(
        	r"""
        	a or (b and c)
            """)
        self.assertAST(owl, python)

    def test_multiple_operators_2(self):
        owl = textwrap.dedent(
            r"""
            (a or b) and c
            """)
        python = textwrap.dedent(
        	r"""
        	(a or b) and c
            """)
        self.assertAST(owl, python)
