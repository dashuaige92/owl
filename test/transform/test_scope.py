import unittest
import textwrap

from owl import transform
from test.parse_helper import TransformTestCase

class TestScope(TransformTestCase):

    def test_redeclaration_raises_error(self):
        owl = textwrap.dedent(
            r"""
            int x
            int x
            """)
        self.assertParseError(owl)

    def test_redeclaration_raises_error(self):
        owl = textwrap.dedent(
            r"""
            int f(int x) {
                    int x
            }
            """)
        self.assertParseError(owl)

    def test_redeclaration_in_new_scope(self):
        owl = textwrap.dedent(
            r"""
            int x
            int f(int z) {
                int x
                x = 1
            }
            """)
        python = textwrap.dedent(
            r"""
            _x = 0
            def _f(__z):
                global _x
                __x = 0
                __x = 1
            """)
        self.assertTransformedAST(owl, python, transform_filters=[transform.StandardLibraryAdder])

    def test_global_accessibility_in_new_scope(self):
        owl = textwrap.dedent(
            r"""
            int x
            int f(int z) {
                int y
                x = 1
            }
            """)
        python = textwrap.dedent(
            r"""
            _x = 0
            def _f(__z):
                global _x
                __y = 0
                _x = 1
            """)
        self.assertTransformedAST(owl, python, transform_filters=[transform.StandardLibraryAdder])

    def test_redeclaration_in_new_scope_after_assignment(self):
        owl = textwrap.dedent(
            r"""
            int x
            int f(int z) {
                x = 1
                int x
            }
            """)
        python = textwrap.dedent(
            r"""
            _x = 0
            def _f(__z):
                global _x
                _x = 1
                __x = 0
            """)
        self.assertTransformedAST(owl, python, transform_filters=[transform.StandardLibraryAdder])
