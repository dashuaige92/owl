import unittest
import textwrap

from test.parse_helper import ParserTestCase

class TestArithmeticParen(ParserTestCase):
    def test_arithmetic_paren(self):
        owl = textwrap.dedent(
            r"""
            int x = (1 + 2) * 3
            """)
        python = textwrap.dedent(
            r"""
            x = 1 + 2 * 3
            """)
        self.assertAST(owl, python)