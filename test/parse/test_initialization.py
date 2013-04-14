import unittest
import textwrap

from test.parse_helper import ParserTestCase

class TestInitialization(ParserTestCase):

    def test_declare_init(self):
        owl = textwrap.dedent(
            r"""
            string s = "test"
            """)
        python = textwrap.dedent(
            r"""
            s = 'test'
            """)
        self.assertAST(owl, python)

    def test_declare_init_2(self):
        owl = textwrap.dedent(
            r"""
            int x = 1
            """)
        python = textwrap.dedent(
            r"""
            x = 1
            """)
        self.assertAST(owl, python)


    def test_declare_init_3(self):
        owl = textwrap.dedent(
            r"""
            int x
            """)
        python = textwrap.dedent(
            r"""
            x = 0
            """)
        self.assertAST(owl, python)


    def test_declare_init_4(self):
        owl = textwrap.dedent(
            r"""
            bool x
            """)
        python = textwrap.dedent(
            r"""
            x = False
            """)
        self.assertAST(owl, python)



    def test_declare_init_5(self):
		owl = textwrap.dedent(r"""
        list l = ["Andrew"]
        """)
		python = textwrap.dedent(r"""l = ["Andrew"]
        """)
		self.assertAST(owl, python)



