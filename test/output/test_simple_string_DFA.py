import unittest
import textwrap

from test.output_helper import OutputTestCase

class TestSimpleStringDFA(OutputTestCase):

    @unittest.skip("default transition doesn't work")
    def test_simple_string_DFA(self):
        owl = 'examples/simple_string_DFA.owl'
        expected_output = "True\n"
        self.assertOutput(owl, expected_output)
