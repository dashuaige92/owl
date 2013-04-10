import unittest
import textwrap

from test.parse_helper import ParserTestCase

class TestBinaryOperators(ParserTestCase):
    def test_plus(self):
        owl = textwrap.dedent(
            r"""
            1 + 2
            """)
        python = textwrap.dedent(
            r"""
            1 + 2
            """)
        self.assertAST(owl, python)

    def test_minus(self):
        owl = textwrap.dedent(
            r"""
            2 - 1
            """)
        python = textwrap.dedent(
            r"""
            2 - 1
            """)
        self.assertAST(owl, python)

    def test_times(self):
        owl = textwrap.dedent(
            r"""
            1 * 2
            """)
        python = textwrap.dedent(
            r"""
            1 * 2
            """)
        self.assertAST(owl, python)

    def test_divide(self):
        owl = textwrap.dedent(
            r"""
            2 / 1
            """)
        python = textwrap.dedent(
            r"""
            2 / 1
            """)
        self.assertAST(owl, python)
