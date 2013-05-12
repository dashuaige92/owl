import unittest
import textwrap
import hashlib

from test.parse_helper import TransformTestCase

class TestMachine(TransformTestCase):

    def transition_name(self, left, right, arg=None):
        if arg is None:
            return '_%s_%s' % (left, right)
        trans = hashlib.md5(arg).hexdigest() if len(arg) > 0 else ''
        return '_%s_%s_%s' % (left, right, trans)

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

    def test_machine_error_1(self):
        owl = textwrap.dedent(
        r"""
        machine m1 = {
            node a
            node a
        }
        """)
        self.assertParseError(owl)

    def test_machine_error_2(self):
        owl = textwrap.dedent(
        r"""
        machine m1 = {
            node a
            enter(b) {
            }
        }
        """)
        self.assertParseError(owl)

    def test_machine_error_3(self):
        owl = textwrap.dedent(
        r"""
        machine m1 = {
            node a
            a() -> b
        }
        """)
        self.assertParseError(owl)

    def test_machine_error_4(self):
        owl = textwrap.dedent(
        r"""
        machine m1 = {
            node a
        }
        machine m2 = {
            node a
        }
        """)
        self.assertParseError(owl)

    def test_machine_error_5(self):
        owl = textwrap.dedent(
        r"""
        machine m1 = {
            node a
        }
        machine m1 = {
            node b
        }
        """)
        self.assertParseError(owl)

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

            def trans{ab_1}(groups):
                pass
            
            {ab_1} = Transition(a, b, '1')
            {ab_1}.on_enter += trans{ab_1}

            m3 = Automaton([a,b],[{ab_1}],a)

            """.format(
                ab_1 = self.transition_name('a', 'b', '1'),
            ))

        self.assertTransformedAST(owl, python)

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
            
            def trans{ab_1}(groups):
                print("hello")

            {ab_1} = Transition(a, b, '1')
            {ab_1}.on_enter += trans{ab_1}
            
            m4 = Automaton([a,b],[{ab_1}],a)

            """).format(
                ab_1 = self.transition_name('a', 'b', '1'),
            )

        self.assertTransformedAST(owl, python)

    def test_machine_func(self):
        owl = textwrap.dedent(r"""
            machine m5 = {
                node a
                enter(a) {
                    print("world")
                }
            }
            """)

        python = textwrap.dedent(r"""
            a = State()

            def func_enter_a():
                print("world")
            
            a.on_enter += func_enter_a

            m5 = Automaton([a],[],a)

            """)

        self.assertTransformedAST(owl, python)

    def test_machine_func_default_trans(self):
        owl = textwrap.dedent(r"""
            machine m5 = {
                node a
                a() -> a {
                    print("invalid input")
                }
            }
            """)

        python = textwrap.dedent(r"""
            a = State()
            def trans{aa_default}(groups):
                print("invalid input")

            {aa_default} = Transition(a, a )
            {aa_default}.on_enter += trans{aa_default}

            m5 = Automaton([a], [{aa_default}], a)

            """.format(
                aa_default = self.transition_name('a', 'a'),
            ))

        self.assertTransformedAST(owl, python)


