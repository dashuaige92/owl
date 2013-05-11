import unittest
import textwrap

from test.parse_helper import ParserTestCase

class TestSelectionStatements(ParserTestCase):

    def test_if_statements(self):
        owl = textwrap.dedent(
            r"""
            if(True) { 
                print("it was true")
            }
            """)
        python = textwrap.dedent(
            r"""
            if True:
                print "it was true"
            """)
        self.assertAST(owl, python)

    def test_if_else_statements(self):
        owl = textwrap.dedent(
            r"""
            if(True) {
                print("it was true") 
            } else {
                print("it was false")
            }
            """)
        python = textwrap.dedent(
            r"""
            if True:
                print "it was true"
            else:
                print "it was false"
            """)
        self.assertAST(owl, python)

    def test_if_else_statements2(self):
        owl = textwrap.dedent(
            r"""
            if(x == 3) {
                print("it's 3")
            } else {
                print("it's not 3")
            }
            """)
        python = textwrap.dedent(
            r"""
            if x == 3:
                print "it's 3"
            else:
                print "it's not 3"
            """)
        self.assertAST(owl, python)
        