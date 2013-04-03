import unittest
import textwrap

from test.parse_helper import ParserTestCase

class TestHelloWorld(ParserTestCase):
    def test_hello_world(self):
        owl = textwrap.dedent(r"""
        print("Hello, world!")
        """)
        python = textwrap.dedent(r"""
        print 'Hello, world!'
        """)
        self.assertAST(owl, python)
