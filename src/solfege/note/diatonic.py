from __future__ import annotations

import unittest

from solfege.interval.diatonic import DiatonicInterval, TestDiatonicInterval
from solfege.note.base import AbstractNote


class DiatonicNote(AbstractNote, DiatonicInterval):
    """A diatonic note"""
    # Saved as the interval from middle C
    IntervalClass = DiatonicInterval

    def get_interval_name(self):
        return ["C", "D", "E", "F", "G", "A", "B"][self.get_number() % 7]


class TestDiatonicNote(TestDiatonicInterval):
    C4 = DiatonicNote(0)
    D4 = DiatonicNote(1)
    B3 = DiatonicNote(-1)
    E4 = DiatonicNote(2)
    F4 = DiatonicNote(3)
    C5 = DiatonicNote(7)
    B4 = DiatonicNote(6)
    D3 = DiatonicNote(-6)
    C3 = DiatonicNote(-7)
    B2 = DiatonicNote(-8)

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
        self.assertEquals(self.D4 + self.third, self.F4)
        self.assertEquals(self.third + self.D4, self.F4)
        with self.assertRaises(Exception):
            _ = self.D4 + self.D4

    def test_neg(self):
        with self.assertRaises(Exception):
            _ = -self.D4

    def test_sub(self):
        self.assertEquals(self.F4 - self.third, self.D4)
        self.assertEquals(self.F4 - self.D4, self.third)
        with self.assertRaises(Exception):
            _ = self.third - self.D4

    def test_lt(self):
        self.assertLess(self.D4, self.F4)
        self.assertLessEqual(self.D4, self.F4)
        self.assertLessEqual(self.D4, self.D4)

    def test_repr(self):
        self.assertEquals(repr(self.D4), "DiatonicNote(value=1)")

    def test_get_octave(self):
        self.assertEquals(self.C4.get_octave(), 0)
        self.assertEquals(self.B4.get_octave(), 0)
        self.assertEquals(self.D3.get_octave(), -1)
        self.assertEquals(self.C3.get_octave(), -1)
        self.assertEquals(self.B2.get_octave(), -2)
        self.assertEquals(self.C5.get_octave(), 1)

    def test_lily_octave(self):
        self.assertEquals(self.C4.lily_octave(), "'")
        self.assertEquals(self.B4.lily_octave(), "'")
        self.assertEquals(self.D3.lily_octave(), "")
        self.assertEquals(self.C3.lily_octave(), "")
        self.assertEquals(self.B2.lily_octave(), ",")
        self.assertEquals(self.C5.lily_octave(), "''")

    def test_add_octave(self):
        self.assertEquals(self.C5.add_octave(-1), self.C4)
        self.assertEquals(self.C4.add_octave(1), self.C5)
        self.assertEquals(self.C5.add_octave(-2), self.C3)
        self.assertEquals(self.C3.add_octave(2), self.C5)

    def test_same_note_in_base_octave(self):
        self.assertEquals(self.C5.get_in_base_octave(), self.C4)
        self.assertEquals(self.C3.get_in_base_octave(), self.C4)
        self.assertEquals(self.C4.get_in_base_octave(), self.C4)
        self.assertEquals(self.D4.get_in_base_octave(), self.D4)
        self.assertEquals(self.B3.get_in_base_octave(), self.B4)

    def test_same_note_in_different_octaves(self):
        self.assertFalse(self.D4.equals_modulo_octave(self.C4))
        self.assertFalse(self.D4.equals_modulo_octave(self.C5))
        self.assertFalse(self.D4.equals_modulo_octave(self.C3))
        self.assertFalse(self.D4.equals_modulo_octave(self.B3))
        self.assertTrue(self.C4.equals_modulo_octave(self.C4))
        self.assertTrue(self.C4.equals_modulo_octave(self.C5))
        self.assertTrue(self.C4.equals_modulo_octave(self.C3))
        self.assertTrue(self.C5.equals_modulo_octave(self.C3))

    def test_get_chromatic(self):
        from solfege.note.chromatic import ChromaticNote
        self.assertEquals(DiatonicNote(0).get_chromatic(), ChromaticNote(0))
        self.assertEquals(DiatonicNote(1).get_chromatic(), ChromaticNote(2))
        self.assertEquals(DiatonicNote(2).get_chromatic(), ChromaticNote(4))
        self.assertEquals(DiatonicNote(3).get_chromatic(), ChromaticNote(5))
        self.assertEquals(DiatonicNote(4).get_chromatic(), ChromaticNote(7))
        self.assertEquals(DiatonicNote(5).get_chromatic(), ChromaticNote(9))
        self.assertEquals(DiatonicNote(6).get_chromatic(), ChromaticNote(11))
        self.assertEquals(DiatonicNote(7).get_chromatic(), ChromaticNote(12))
        self.assertEquals(DiatonicNote(8).get_chromatic(), ChromaticNote(14))
        self.assertEquals(DiatonicNote(9).get_chromatic(), ChromaticNote(16))
        self.assertEquals(DiatonicNote(-1).get_chromatic(), ChromaticNote(-1))
        self.assertEquals(DiatonicNote(-2).get_chromatic(), ChromaticNote(-3))
        self.assertEquals(DiatonicNote(-3).get_chromatic(), ChromaticNote(-5))
        self.assertEquals(DiatonicNote(-4).get_chromatic(), ChromaticNote(-7))
        self.assertEquals(DiatonicNote(-5).get_chromatic(), ChromaticNote(-8))
        self.assertEquals(DiatonicNote(-6).get_chromatic(), ChromaticNote(-10))
        self.assertEquals(DiatonicNote(-7).get_chromatic(), ChromaticNote(-12))
        self.assertEquals(DiatonicNote(-8).get_chromatic(), ChromaticNote(-13))
        self.assertEquals(DiatonicNote(-9).get_chromatic(), ChromaticNote(-15))

    def test_get_interval_name(self):
        self.assertEquals(DiatonicNote(0).get_interval_name(), "C")
        self.assertEquals(DiatonicNote(1).get_interval_name(), "D")
        self.assertEquals(DiatonicNote(2).get_interval_name(), "E")
        self.assertEquals(DiatonicNote(3).get_interval_name(), "F")
        self.assertEquals(DiatonicNote(4).get_interval_name(), "G")
        self.assertEquals(DiatonicNote(5).get_interval_name(), "A")
        self.assertEquals(DiatonicNote(6).get_interval_name(), "B")
        self.assertEquals(DiatonicNote(7).get_interval_name(), "C")
        self.assertEquals(DiatonicNote(8).get_interval_name(), "D")
        self.assertEquals(DiatonicNote(9).get_interval_name(), "E")
        self.assertEquals(DiatonicNote(-1).get_interval_name(), "B")
        self.assertEquals(DiatonicNote(-2).get_interval_name(), "A")
        self.assertEquals(DiatonicNote(-3).get_interval_name(), "G")
        self.assertEquals(DiatonicNote(-4).get_interval_name(), "F")
        self.assertEquals(DiatonicNote(-5).get_interval_name(), "E")
        self.assertEquals(DiatonicNote(-6).get_interval_name(), "D")
        self.assertEquals(DiatonicNote(-7).get_interval_name(), "C")
        self.assertEquals(DiatonicNote(-8).get_interval_name(), "B")
        self.assertEquals(DiatonicNote(-9).get_interval_name(), "A")
