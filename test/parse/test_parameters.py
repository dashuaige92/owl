import unittest
import textwrap

from test.parse_helper import ParserTestCase

class TestParameters(ParserTestCase):
	# Do we need to test a single parameter? same as string
	def test_parameter(self):
		owl = textwrap.dedent(r"""
			'a'
		""")
		python = textwrap.dedent(r"""
			'a'
		""")
		self.assertAST(owl, python)
	def test_parameter(self):
		owl = textwrap.dedent(r"""
			test(a, b, c, d)
		""")
		python = textwrap.dedent(r"""
			test(a, b, c, d)
		""")
		self.assertAST(owl, python)
