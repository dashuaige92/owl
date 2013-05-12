import unittest
import textwrap

from test.output_helper import OutputTestCase

class TestEmptyLists(OutputTestCase):

    def test_empty_lists(self):
        owl = 'examples/empty_lists.owl'
        expected_output = "[1, 2, 4]\n[]\n"
        self.assertOutput(owl, expected_output)
