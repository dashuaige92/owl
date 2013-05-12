import unittest
import textwrap

from test.parse_helper import ParserTestCase

class TestMachine(ParserTestCase):

	#Invalid
	def test_machine_step_invalid(self):
		owl = textwrap.dedent(r"""
			string m1
			m1.step("hello there")
			""")
		self.assertParseError(owl)
