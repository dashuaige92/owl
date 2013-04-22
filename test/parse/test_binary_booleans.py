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