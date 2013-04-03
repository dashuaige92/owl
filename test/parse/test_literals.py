import unittest

from test.parse_helper import ParserTestCase

owl = r"""print(3)
"""
python = r"""print 3
"""

class TestHelloWorld(ParserTestCase):
    def test_hello_world(self):
        self.assertAST(owl, python)
