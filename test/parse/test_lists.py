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
