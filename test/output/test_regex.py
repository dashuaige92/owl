import unittest
import textwrap

from test.output_helper import OutputTestCase

class TestRegex(OutputTestCase):

    def test_regex(self):
        owl = 'examples/regex.owl'
        expected_output = "banana\n12345\n"
        self.assertOutput(owl, expected_output)
