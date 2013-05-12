import unittest
import textwrap

from test.output_helper import OutputTestCase

class TestTutorial(OutputTestCase):

    def test_tutorial_variables_and_functions(self):
        owl = 'examples/tutorial_variables_functions.owl'
        expected_output = "Hello world\nHello world\nHello world\n7\n"
        self.assertOutput(owl, expected_output)

    def test_tutorial_lists(self):
        owl = 'examples/tutorial_lists.owl'
        expected_output = "cat\n"
        self.assertOutput(owl, expected_output)

    def test_tutorial_if_statements(self):
        owl = 'examples/tutorial_if_statements.owl'
        expected_output = "False\n"
        self.assertOutput(owl, expected_output)

    def test_tutorial_loops(self):
        owl = 'examples/tutorial_loops.owl'
        expected_output = "0\n1\n2\n3\n4\n5\n0\n1\n2\n3\n4\n5\n"
        self.assertOutput(owl, expected_output)

    def test_tutorial_machine_hello_world(self):
        owl = 'examples/tutorial_machine_hello_world.owl'
        expected_output = "Hello world\nHello world\n"
        self.assertOutput(owl, expected_output)

    def test_tutorial_pattern_matching(self):
        owl = 'examples/tutorial_pattern_matching.owl'
        expected_output = "Still looking...\nStill looking...\nStill looking...\nFound match!\nSo far we have found 1 matches!\nStill looking...\nStill looking...\nStill looking...\nStill looking...\nFound match!\nSo far we have found 2 matches!\nStill looking...\nStill looking...\nStill looking...\nStill looking...\nStill looking...\nStill looking...\nStill looking...\nStill looking...\nStill looking...\nStill looking...\nFound match!\nSo far we have found 3 matches!\nStill looking...\nStill looking...\nStill looking...\nStill looking...\n"
        self.assertOutput(owl, expected_output)