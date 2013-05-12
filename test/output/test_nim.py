import unittest
import textwrap

from test.output_helper import OutputTestCase

class TestNim(OutputTestCase):

    def test_nim(self):
        owl = 'examples/nim.owl'
        owl_input = '3, 0\n4, 1\n5, 2\n'
        output = textwrap.dedent(
            r"""

            Current stacks:
            3 
            4 
            5 
            Remove X chips from stack Y (X, Y): 

            Current stacks:
            0 
            4 
            5 
            Remove X chips from stack Y (X, Y): 

            Current stacks:
            0 
            0 
            5 
            Remove X chips from stack Y (X, Y): 
            You win!

            Current stacks:
            0 
            0 
            0 
            Remove X chips from stack Y (X, Y): 
            """)[1:]
        self.assertOutput(owl, output, owl_input)
