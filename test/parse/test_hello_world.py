import unittest

from test.parse_helper import ParserTestCase

owl = r"""print("Hello, world!")
"""
python = r"""print 'Hello, world!'
"""

class TestHelloWorld(ParserTestCase):
    def test_hello_world(self):
        self.assertAST(owl, python)
