import unittest
import textwrap

from test.output_helper import OutputTestCase

class TestIfStatements(OutputTestCase):

    def test_if_statements(self):
        owl = 'examples/if_statements.owl'
        expected_output = "it's 3\n"
        self.assertOutput(owl, expected_output)
