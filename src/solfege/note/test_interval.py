from src.solfege.interval.test_interval import TestInterval
from .note import *

class TestNote(TestInterval):
    C3 = Note(chromatic=-12, diatonic=-7)
    B3 = Note(chromatic=-1, diatonic=-1)
    A3 = Note(chromatic=-3, diatonic=-2)
    B3_flat = Note(chromatic=-2, diatonic=-1)
    C4 = Note(chromatic=0, diatonic=0)
    C4_sharp = Note(chromatic=1, diatonic=1)
    D4 = Note(chromatic=2, diatonic=1)
    D4_sharp = Note(chromatic=3, diatonic=1)
    E4b = Note(chromatic=3, diatonic=2)
    E4 = Note(chromatic=4, diatonic=2)
    F4 = Note(chromatic=5, diatonic=3)
    C5 = Note(chromatic=12, diatonic=7)

    def test_lily(self):
        self.assertEquals(self.C4.lily_in_scale(), "c'")
        self.assertEquals(self.F4.lily_in_scale(), "f'")

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
        with self.assertRaises(Exception):
            _ = self.D4 + self.C4
        self.assertEquals(self.D4 + third_minor, self.F4)
        sum_ = third_minor + self.D4
        self.assertEquals(sum_, self.F4)

    def test_neg(self):
        with self.assertRaises(Exception):
            _ = -self.D4

    def test_sub(self):
        self.assertEquals(self.F4 - self.D4, third_minor)
        self.assertEquals(self.F4 - third_minor, self.D4)
        with self.assertRaises(Exception):
            _ = third_minor - self.C4

    def test_lt(self):
        self.assertLess(self.C4_sharp, self.D4)
        self.assertLessEqual(self.C4_sharp, self.D4)
        self.assertLessEqual(self.D4, self.D4)

    def test_repr(self):
        self.assertEquals(repr(self.D4), "Note(chromatic = 2, diatonic = 1)")

    def test_get_octave(self):
        self.assertEquals(self.C4.get_octave(), 0)
        self.assertEquals(self.C3.get_octave(), -1)
        self.assertEquals(self.C5.get_octave(), 1)

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

    def test_same_note_in_different_octaves(self):
        self.assertFalse(self.D4.equals_modulo_octave(self.C4))
        self.assertFalse(self.D4.equals_modulo_octave(self.C5))
        self.assertFalse(self.D4.equals_modulo_octave(self.C3))
        self.assertTrue(self.C4.equals_modulo_octave(self.C4))
        self.assertTrue(self.C4.equals_modulo_octave(self.C5))
        self.assertTrue(self.C4.equals_modulo_octave(self.C3))
        self.assertTrue(self.C5.equals_modulo_octave(self.C3))

    def test_lily_black(self):
        self.assertEquals(self.C4.lily_in_scale(), "c'")
        self.assertEquals(self.C3.lily_in_scale(), "c")
        self.assertEquals(self.C5.lily_in_scale(), "c''")
        self.assertEquals(self.B3.lily_in_scale(), "b")

    def test_is_black_key(self):
        self.assertFalse(self.C4.is_black_key_on_piano())
        self.assertTrue(self.C4_sharp.is_black_key_on_piano())

    def test_adjacent(self):
        with self.assertRaises(Exception):
            self.assertTrue(self.C4.adjacent(self.C4))
        self.assertTrue(self.C4.adjacent(self.B3))
        self.assertTrue(self.C4.adjacent(self.B3_flat))
        self.assertTrue(self.C4.adjacent(self.C4_sharp))
        self.assertTrue(self.C4.adjacent(self.D4))
        self.assertTrue(self.C4.adjacent(self.D4_sharp))
        self.assertFalse(self.C4.adjacent(self.A3))
        self.assertFalse(self.C4.adjacent(self.E4))

        self.assertTrue(self.B3.adjacent(self.C4))
        self.assertTrue(self.B3_flat.adjacent(self.C4))
        self.assertTrue(self.C4_sharp.adjacent(self.C4))
        self.assertTrue(self.D4.adjacent(self.C4))
        self.assertTrue(self.D4_sharp.adjacent(self.C4))
        self.assertFalse(self.A3.adjacent(self.C4))
        self.assertFalse(self.E4.adjacent(self.C4))

        self.assertFalse(Note("C4#").adjacent(Note("B3♭")))
        self.assertFalse(Note("D4").adjacent(Note("B3")))
        self.assertFalse(Note("F").adjacent(Note("D")))
        self.assertFalse(Note("F#").adjacent(Note("D#")))
        self.assertFalse(Note("G").adjacent(Note("E")))
        self.assertTrue(Note("D#").adjacent(Note("C")))
        self.assertTrue(Note("E").adjacent(Note("C#")))
        self.assertTrue(Note("G#").adjacent(Note("F")))
        self.assertTrue(Note("A").adjacent(Note("G♭")))
        self.assertTrue(Note("A#").adjacent(Note("G")))
        self.assertTrue(Note("B").adjacent(Note("A♭")))

    def test_from_name(self):
        self.assertEquals(Note("C"), Note(chromatic=0, diatonic=0))
        self.assertEquals(Note("C4"), Note(chromatic=0, diatonic=0))
        self.assertEquals(Note("B3#"), Note(chromatic=0, diatonic=-1))
        self.assertEquals(Note("B#3"), Note(chromatic=0, diatonic=-1))

        self.assertEquals(Note("C♭"), Note(chromatic=-1, diatonic=0))
        self.assertEquals(Note("C4♭"), Note(chromatic=-1, diatonic=0))
        self.assertEquals(Note("C♭4"), Note(chromatic=-1, diatonic=0))
        self.assertEquals(Note("B3"), Note(chromatic=-1, diatonic=-1))

    def test_from_name_to_name(self):
        self.assertEquals(Note("C4").get_full_name(), "C  4")
        self.assertEquals(Note("C♭4").get_full_name(), "C♭ 4")

    def test_simplest_enharmonic(self):
        self.assertEquals(Note("C").simplest_enharmonic(), Note("C"))
        self.assertEquals(Note("C♭").simplest_enharmonic(), Note("B3"))
        self.assertEquals(Note("B3#").simplest_enharmonic(), Note("C"))
        self.assertEquals(Note("C#").simplest_enharmonic(), Note("C#"))
        self.assertEquals(Note("C##").simplest_enharmonic(), Note("D"))
        self.assertEquals(Note("D♭").simplest_enharmonic(), Note("D♭"))
        self.assertEquals(Note("D♭♭").simplest_enharmonic(), Note("C"))

    def test_canonize(self):
        self.assertEquals(Note("C").canonize(for_sharp=True), Note("C"))
        self.assertEquals(Note("C♭").canonize(for_sharp=True), Note("B3"))
        self.assertEquals(Note("B3#").canonize(for_sharp=True), Note("C"))
        self.assertEquals(Note("C#").canonize(for_sharp=True), Note("C#"))
        self.assertEquals(Note("C##").canonize(for_sharp=True), Note("D"))
        self.assertEquals(Note("D♭").canonize(for_sharp=True), Note("C#"))
        self.assertEquals(Note("D♭♭").canonize(for_sharp=False), Note("C"))
        self.assertEquals(Note("C").canonize(for_sharp=False), Note("C"))
        self.assertEquals(Note("C♭").canonize(for_sharp=False), Note("B3"))
        self.assertEquals(Note("B3#").canonize(for_sharp=False), Note("C"))
        self.assertEquals(Note("C#").canonize(for_sharp=False), Note("D♭"))
        self.assertEquals(Note("C##").canonize(for_sharp=False), Note("D"))
        self.assertEquals(Note("D♭").canonize(for_sharp=False), Note("D♭"))
        self.assertEquals(Note("D♭♭").canonize(for_sharp=False), Note("C"))

    # todo Test wwith color
