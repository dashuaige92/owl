import unittest
import textwrap

from test.output_helper import OutputTestCase

class TestBinaryModThreeDFA(OutputTestCase):
    def test_binary_mod_three(self):
        owl = 'examples/binary_mod_three.owl'
        output = textwrap.dedent(
            r"""
            is 0 mod 3.
            1
            is 1 mod 3.
            11
            is 0 mod 3.
            111
            is 1 mod 3.
            1110
            is 2 mod 3.
            11101
            is 2 mod 3.
            """)[1:]
        self.assertOutput(owl, output)
