import unittest
import textwrap

from test.parse_helper import ParserTestCase

class TestInitialization(ParserTestCase):

    def test_declare_init_int(self):
        owl = textwrap.dedent(
            r"""
            int x = 1
            """)
        python = textwrap.dedent(
            r"""
            x = 1
            """)
        self.assertAST(owl, python)

    def test_declare_init_bool(self):
        owl = textwrap.dedent(
            r"""
            bool b = True
            """)
        python = textwrap.dedent(
            r"""
            b = True
            """)
        self.assertAST(owl, python)
    def test_declare_init_float(self):
        owl = textwrap.dedent(
            r"""
            float f = 1.5
            """)
        python = textwrap.dedent(
            r"""
            f = 1.5
            """)
        self.assertAST(owl, python)

    def test_declare_init_string(self):
        owl = textwrap.dedent(
            r"""
            string s = "test"
            """)
        python = textwrap.dedent(
            r"""
            s = 'test'
            """)
        self.assertAST(owl, python)

    def test_declare_init_list(self):
        owl = textwrap.dedent(r"""
        list l = ["Andrew"]
        """)
        python = textwrap.dedent(r"""l = ["Andrew"]
        """)
        self.assertAST(owl, python)

    # Default Initializations

    def test_declare_int(self):
        owl = textwrap.dedent(
            r"""
            int x
            """)
        python = textwrap.dedent(
            r"""
            x = 0
            """)
        self.assertAST(owl, python)

    def test_declare_bool(self):
        owl = textwrap.dedent(
            r"""
            bool x
            """)
        python = textwrap.dedent(
            r"""
            x = False
            """)
        self.assertAST(owl, python)

    def test_declare_float(self):
        owl = textwrap.dedent(
            r"""
            float x
            """)
        python = textwrap.dedent(
            r"""
            x = 0
            """)
        self.assertAST(owl, python)

    def test_declare_string(self):
        owl = textwrap.dedent(
            r"""
            string s
            """)
        python = textwrap.dedent(
            r"""
            s = ""
            """)
        self.assertAST(owl, python)

    def test_declare_list(self):
        owl = textwrap.dedent(
            r"""
            list l
            """)
        python = textwrap.dedent(
            r"""
            l = []
            """)
        self.assertAST(owl, python)




   



