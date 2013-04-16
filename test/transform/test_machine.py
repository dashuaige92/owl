import unittest
import textwrap

from test.parse_helper import TransformTestCase

class TestMachine(TransformTestCase):

    def test_machine_without_nodes_raises_error(self):
        owl = textwrap.dedent(
            r"""
            machine m1 = {
            }
            """)
        self.assertTransformError(owl)

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
        
        self.assertTransformedAST(owl, python)

    @unittest.skip("Refactoring")
    def test_machine_trans(self):
        owl = textwrap.dedent(r"""
            machine m3 = {
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

            m3 = Automaton([a,b],[ab],a)

            """)

        self.assertTransformedAST(owl, python)

    @unittest.skip("Refactoring")
    def test_machine_trans_2(self):
        owl = textwrap.dedent(r"""
            machine m4 = {
                node a
                node b
                a("1") -> b {
                    print("hello")
                }
            }
            """)

        python = textwrap.dedent(r"""
            a = State()
            b = State()
            
            def trans_ab():
                print("hello")

            ab = Transition(a, b, trans_ab)

            m4 = Automaton([a,b],[ab],a)

            """)

        self.assertTransformedAST(owl, python)


