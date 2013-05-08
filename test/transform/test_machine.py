import unittest
import textwrap

from test.parse_helper import TransformTestCase

class TestMachine(TransformTestCase):

    def test_machine_without_nodes_raises_error(self):
        owl = textwrap.dedent(
            r"""
            machine m1 = {}
            """)
        self.assertTransformError(owl)

    def test_machine_without_nodes_raises_error_2(self):
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

    #@unittest.skip("Refactoring")
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

            def trans_a_b_1():
                pass
            
            _a_b_1 = Transition(a, b, lambda _x: (_x == '1') )
            _a_b_1.on_enter += trans_a_b_1

            m3 = Automaton([a,b],[_a_b_1],a)

            """)

        self.assertTransformedAST(owl, python)

    #@unittest.skip("Refactoring")
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
            
            def trans_a_b_1():
                print("hello")

            _a_b_1 = Transition(a, b, lambda _x: (_x == '1') )
            _a_b_1.on_enter += trans_a_b_1
            
            m4 = Automaton([a,b],[_a_b_1],a)

            """)

        self.assertTransformedAST(owl, python)


    #@unittest.skip("Not yet implemented")
    def test_machine_func(self):
        owl = textwrap.dedent(r"""
            machine m5 = {
                node a
                node b
                enter(a) {
                    print("world")
                }
                a("1") -> b {
                    print("hello")
                }
            }
            """)

        python = textwrap.dedent(r"""
            a = State()
            b = State()

            def func_a():
                print("world")
            
            a.on_enter += func_a

            def trans_a_b_1():
                print("hello")

            _a_b_1 = Transition(a, b, lambda _x: (_x == '1') )
            _a_b_1.on_enter += trans_a_b_1

            m5 = Automaton([a,b],[_a_b_1],a)

            """)

        self.assertTransformedAST(owl, python)


