from .lilyable import *


class TestLilyable(unittest.TestCase):
    def test_lily(self):
        self.assertEquals("aes", LiteralLilyable("aes").lily_in_scale())

    def test_eq_diff_class(self):
        class MockLily(Lilyable):
            def lily_in_scale(self):
                return "aes"

        self.assertEquals(LiteralLilyable("aes"), MockLily())

    def test_eq(self):
        self.assertEquals(LiteralLilyable("aes"), LiteralLilyable("aes"))
