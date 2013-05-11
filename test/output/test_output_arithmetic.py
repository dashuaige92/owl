import unittest
import textwrap

from test.output_helper import OutputTestCase

class TestOutputArithmetic(OutputTestCase):

    def test_output_arithmetic(self):
        owl = 'examples/arithmetic.owl'
        expected_output = '3\n4\n7\n7\n'
        self.assertOutput(owl, expected_output)