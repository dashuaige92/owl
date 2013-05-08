import unittest
import textwrap

from test.output_helper import OutputTestCase

class TestOutputHelloWorld(OutputTestCase):
	def test_output_hello_world(self):
		owl = 'examples/hello_world.owl'
		expected_output = 'Hello, world!\n'
		self.assertOutput(owl, expected_output)