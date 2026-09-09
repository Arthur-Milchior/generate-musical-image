import unittest
from _lily.Lilyable.lilyable import *


class TestLilyable(unittest.TestCase):
    def test_lily(self):
        """`LiteralLilyable.lily()` returns the fixed string it was constructed with."""
        self.assertEqual("aes", LiteralLilyable("aes").lily())

    def test_eq_diff_class(self):
        """`Lilyable.__eq__` compares by generated code, so instances of unrelated subclasses producing the same
        code are equal."""
        class MockLily(Lilyable):
            def lily(self):
                """Fixed code `"aes"`, matching `LiteralLilyable("aes")`."""
                return "aes"

        self.assertEqual(LiteralLilyable("aes"), MockLily())

    def test_eq(self):
        """Two `LiteralLilyable`s with the same fixed string are equal."""
        self.assertEqual(LiteralLilyable("aes"), LiteralLilyable("aes"))
