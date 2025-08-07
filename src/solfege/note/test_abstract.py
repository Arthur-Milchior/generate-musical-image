from .abstract import *

class TestBaseNote(TestBaseInterval):
    C4 = AbstractNote(0)
    D4 = AbstractNote(1)
    B3 = AbstractNote(-1)
    E4 = AbstractNote(2)
    F4 = AbstractNote(3)

    def test_is_note(self):
        self.assertTrue(self.C4.is_note())

    def test_has_number(self):
        self.assertTrue(self.C4.has_number())

    def test_get_number(self):
        self.assertEquals(self.C4.get_number(), 0)

    def test_equal(self):
        self.assertEquals(self.C4, self.C4)
        self.assertNotEquals(self.D4, self.C4)
        self.assertEquals(self.D4, self.D4)

    def test_add(self):
        self.assertEquals(self.D4 + self.deux, self.F4)
        self.assertEquals(self.deux + self.D4, self.F4)
        with self.assertRaises(Exception):
            _ = self.D4 + self.D4

    def test_neg(self):
        with self.assertRaises(Exception):
            _ = -self.D4

    def test_sub(self):
        self.assertEquals(self.F4 - self.deux, self.D4)
        self.assertEquals(self.F4 - self.D4, self.deux)

    def test_lt(self):
        self.assertLess(self.D4, self.deux)
        self.assertLessEqual(self.D4, self.deux)
        self.assertLessEqual(self.D4, self.D4)

    def test_repr(self):
        self.assertEquals(repr(self.D4), "AbstractNote(value=1)")

    def test_low_and_high(self):
        self.assertEquals(low_and_high(self.C4, self.C4), (self.C4, self.C4))
        self.assertEquals(low_and_high(self.D4, self.C4), (self.C4, self.D4))
        self.assertEquals(low_and_high(self.C4, self.D4), (self.C4, self.D4))

    def test_pinky_and_thumb(self):
        self.assertEquals(pinky_and_thumb_side(self.C4, self.C4, for_right_hand=False), (self.C4, self.C4))
        self.assertEquals(pinky_and_thumb_side(self.D4, self.C4, for_right_hand=False), (self.C4, self.D4))
        self.assertEquals(pinky_and_thumb_side(self.C4, self.D4, for_right_hand=False), (self.C4, self.D4))
        self.assertEquals(pinky_and_thumb_side(self.C4, self.C4, for_right_hand=True), (self.C4, self.C4))
        self.assertEquals(pinky_and_thumb_side(self.D4, self.C4, for_right_hand=True), (self.D4, self.C4))
        self.assertEquals(pinky_and_thumb_side(self.C4, self.D4, for_right_hand=True), (self.D4, self.C4))
