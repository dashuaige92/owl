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
        range(10,12)
        """)
        python = textwrap.dedent(r"""
        range(10,12)
        """)
        self.assertAST(owl, python)

    def test_expression_in_index(self):
        owl = textwrap.dedent(
            r"""
            int[] s = [3, 4]
            s[0]
            s[1]
            s[0+1]

            """)
        python = textwrap.dedent(
            r"""
            s = [3, 4]
            s[0]
            s[1]
            s[0+1]            
            """)
        self.assertAST(owl, python)

    def test_list_index(self):
        owl = textwrap.dedent(
            r"""
            int[] a = [2, 3]
            a[0] = 1
            """)
        python = textwrap.dedent(
            r"""
            a = [2,3]
            a[0] = 1
            """)
        self.assertAST(owl, python)

    def test_list_print(self):
        owl = textwrap.dedent(
            r"""
            int[] b = [1, 3]
            print(b[1])
            """)
        python = textwrap.dedent(
            r"""
            b = [1,3]
            print(b[1])
            """)
        self.assertAST(owl, python)    


    def test_lists_error(self):
        owl = textwrap.dedent(r"""
        [,"Kenneth"]
        """)
        
        self.assertParseError(owl)
