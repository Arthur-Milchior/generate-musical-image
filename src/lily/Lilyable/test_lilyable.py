import unittest
from lily.Lilyable.lilyable import *


class TestLilyable(unittest.TestCase):
    def test_lily(self):
        self.assertEqual("aes", LiteralLilyable("aes").lily())

    def test_eq_diff_class(self):
        class MockLily(Lilyable):
            def lily(self):
                return "aes"

        self.assertEqual(LiteralLilyable("aes"), MockLily())

    def test_eq(self):
        self.assertEqual(LiteralLilyable("aes"), LiteralLilyable("aes"))
