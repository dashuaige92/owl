import unittest
import textwrap

from test.output_helper import OutputTestCase

class TestGroups(OutputTestCase):

    def test_groups(self):
        owl = 'examples/groups.owl'
        expected_output = "\nhello\n\n"
        self.assertOutput(owl, expected_output)
