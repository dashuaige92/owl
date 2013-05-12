import unittest
import subprocess

class OutputTestCase(unittest.TestCase):
    """A test case for testing the output of Owl programs.
    """
    def assertOutput(self, owl_file, expected_output, owl_input=''):
        output = ''
        p = subprocess.Popen(['python','run.py', owl_file],
                                 universal_newlines=True,
                                 stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE)

        p.stdin.write(owl_input)

        output = p.stdout.read()
        if output != expected_output:
            raise AssertionError('Owl output does not match expected output!' +
                                 '\n\nOutput:\n' + repr(output) +
                                 '\n\nExpected:\n' + repr(expected_output)
                                )
