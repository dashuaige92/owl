import unittest
import textwrap

from test.parse_helper import ParserTestCase

class TestLists(ParserTestCase):
    def test_lists(self):
        owl = textwrap.dedent(r"""
        ["Andrew"]
        """)
        python = textwrap.dedent(r"""
        ["Andrew"]
        """)
        self.assertAST(owl, python)

    def test_lists2(self):
        owl = textwrap.dedent(r"""
        ["Andrew","Kenneth",1,2]
        """)
        python = textwrap.dedent(r"""
        ["Andrew","Kenneth",1,2]
        """)
        self.assertAST(owl, python)

    def test_lists_range(self):
        owl = textwrap.dedent(r"""
        range (10)
        """)
        python = textwrap.dedent(r"""
        range(10)
        """)
        self.assertAST(owl, python)

    def test_lists_range2(self):
        owl = textwrap.dedent(r"""
        range (10,12)
        """)
        python = textwrap.dedent(r"""
        range(10,12)
        """)
        self.assertAST(owl, python)

    @unittest.skip("Not implemented")
    def test_expression_in_index(self):
        owl = textwrap.dedent(
            r"""
            list s = [3, 4]
            s[0]
            s[0 + 1]
            """)
        python = textwrap.dedent(
            r"""
            s = [3, 4]
            s[0]
            s[0 + 1]
            """)
        self.assertAST(owl, python)

    def test_lists_error(self):
        owl = textwrap.dedent(r"""
        [,"Kenneth"]
        """)
        
        self.assertParseError(owl)
