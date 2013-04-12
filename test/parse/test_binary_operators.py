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

    def test_modulo(self):
        owl = textwrap.dedent(
            r"""
            2 % 1
            """)
        python = textwrap.dedent(
            r"""
            2 % 1
            """)
        self.assertAST(owl, python)

    def test_eq(self):
        owl = textwrap.dedent(
            r"""
            2 == 1
            """)
        python = textwrap.dedent(
            r"""
            2 == 1
            """)
        self.assertAST(owl, python)

    def test_neq(self):
        owl = textwrap.dedent(
            r"""
            2 != 1
            """)
        python = textwrap.dedent(
            r"""
            2 != 1
            """)
        self.assertAST(owl, python)

    def test_lt(self):
        owl = textwrap.dedent(
            r"""
            2 < 1
            """)
        python = textwrap.dedent(
            r"""
            2 < 1
            """)
        self.assertAST(owl, python)

    def test_lteq(self):
        owl = textwrap.dedent(
            r"""
            2 <= 1
            """)
        python = textwrap.dedent(
            r"""
            2 <= 1
            """)
        self.assertAST(owl, python)

    def test_gt(self):
        owl = textwrap.dedent(
            r"""
            2 > 1
            """)
        python = textwrap.dedent(
            r"""
            2 > 1
            """)
        self.assertAST(owl, python)

    def test_gteq(self):
        owl = textwrap.dedent(
            r"""
            2 >= 1
            """)
        python = textwrap.dedent(
            r"""
            2 >= 1
            """)
        self.assertAST(owl, python)

    def test_multiple_operators_raises_error(self):
        self.assertParseError('2 >>== 1')
