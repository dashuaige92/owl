import unittest
import subprocess

class OutputTestCase(unittest.TestCase):
    """A test case for testing the output of Owl programs.
    """
    def assertOutput(self, owl_file, expected_output):
        proc1 = subprocess.Popen(['python','compile.py',owl_file],stdout=subprocess.PIPE)
        compiled = ''
        while True:
            line = proc1.stdout.readline()
            if line != '':
                compiled = compiled + line
            else:
                break

        f = open('temp.py', 'w')
        f.write(compiled)
        f.close()

        output = ''
        proc2 = subprocess.Popen(['python','temp.py'],stdout=subprocess.PIPE)
        while True:
            line = proc2.stdout.readline()
            if line != '':
                output = output + line
            else:
                break

        if output.rstrip() != expected_output.rstrip():
            raise AssertionError('Owl output does not match expected output!' +
                                 '\n\nOutput:\n' + output +
                                 '\n\nExpected:\n' + expected_output
                                )
