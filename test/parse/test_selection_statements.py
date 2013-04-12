import unittest
import textwrap

from test.parse_helper import ParserTestCase

class TestSelectionStatements(ParserTestCase):

    @unittest.skip("Not yet implemented")
    def test_if_statements(self):
        owl = textwrap.dedent(
            r"""
            if(true) {
                print("it was true") 
            }
            """)
        python = textwrap.dedent(
            r"""
            if True:
                print "it was true" 
            """)
        self.assertAST(owl, python)

    @unittest.skip("Not yet implemented")
    def test_if_else_statements(self):
        owl = textwrap.dedent(
            r"""
            if(true) {
                print("it was true") 
            }
            else {
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
