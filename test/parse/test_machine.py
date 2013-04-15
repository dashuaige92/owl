import unittest
import textwrap

from test.parse_helper import ParserTestCase

class TestMachine(ParserTestCase):

    def test_machine_trivial(self):
        owl = textwrap.dedent(r"""
            machine m1 = {
            }
            """)

        python = textwrap.dedent(r"""
            m1 = Automaton([],[],None)
            """)
        
        self.assertAST(owl, python)

    def test_machine_simple(self):
        owl = textwrap.dedent(r"""
            machine m2 = {
                node a
                node b
            }
            """)

        python = textwrap.dedent(r"""
            a = State()
            b = State()
            
            m2 = Automaton([a,b],[],a)
            """)
        
        self.assertAST(owl, python)

    @unittest.skip("Not yet implemented")
    def test_machine_trans(self):
        owl = textwrap.dedent(r"""
            machine m = {
                node a
                node b
                a("1") -> b
            }
            """)

        python = textwrap.dedent(r"""
            a = State()
            b = State()

            def trans_ab():
                pass

            ab = Transition(a, b, trans_ab)

            m = Automaton([a,b],[ab],a)

            """)

        self.assertAST(owl, python)


