from src.solfege.interval.test_chromatic import TestChromaticInterval
from .chromatic import *

class TestChromaticNote(TestChromaticInterval):
    C4 = ChromaticNote(0)
    D4 = ChromaticNote(2)
    B3 = ChromaticNote(-1)
    E4 = ChromaticNote(4)
    F4 = ChromaticNote(5)
    C5 = ChromaticNote(12)
    B4 = ChromaticNote(11)
    D3 = ChromaticNote(-10)
    C3 = ChromaticNote(-12)
    B2 = ChromaticNote(-13)

    def setUp(self):
        super().setUp()
        from solfege.note.diatonic import DiatonicNote
        from solfege.note.note import Note
        from solfege.note.alteration import Alteration
        ChromaticNote.RelatedDiatonicClass = DiatonicNote
        ChromaticNote.RelatedSolfegeClass = Note
        ChromaticNote.AlterationClass = Alteration

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
        self.assertEquals(self.D4 + self.third_minor, self.F4)
        self.assertEquals(self.third_minor + self.D4, self.F4)
        with self.assertRaises(Exception):
            _ = self.D4 + self.D4

    def test_neg(self):
        with self.assertRaises(Exception):
            _ = -self.D4

    def test_sub(self):
        self.assertEquals(self.F4 - self.third_minor, self.D4)
        self.assertEquals(self.F4 - self.D4, self.third_minor)
        with self.assertRaises(Exception):
            _ = self.third_minor - self.D4

    def test_lt(self):
        self.assertLess(self.D4, self.F4)
        self.assertLessEqual(self.D4, self.F4)
        self.assertLessEqual(self.D4, self.D4)

    def test_repr(self):
        self.assertEquals(repr(self.D4), "ChromaticNote(value=2)")

    def test_get_octave(self):
        self.assertEquals(self.C4.get_octave(), 0)
        self.assertEquals(self.B4.get_octave(), 0)
        self.assertEquals(self.D3.get_octave(), -1)
        self.assertEquals(self.C3.get_octave(), -1)
        self.assertEquals(self.B2.get_octave(), -2)
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

    def test_get_interval_name(self):
        self.assertEquals(ChromaticNote(0).get_name_up_to_octave(), "C")
        self.assertEquals(ChromaticNote(1).get_name_up_to_octave(), "C#")
        self.assertEquals(ChromaticNote(2).get_name_up_to_octave(), "D")
        self.assertEquals(ChromaticNote(3).get_name_up_to_octave(), "E♭")
        self.assertEquals(ChromaticNote(4).get_name_up_to_octave(), "E")
        self.assertEquals(ChromaticNote(5).get_name_up_to_octave(), "F")
        self.assertEquals(ChromaticNote(6).get_name_up_to_octave(), "F#")
        self.assertEquals(ChromaticNote(7).get_name_up_to_octave(), "G")
        self.assertEquals(ChromaticNote(8).get_name_up_to_octave(), "A♭")
        self.assertEquals(ChromaticNote(9).get_name_up_to_octave(), "A")
        self.assertEquals(ChromaticNote(10).get_name_up_to_octave(), "B♭")
        self.assertEquals(ChromaticNote(11).get_name_up_to_octave(), "B")
        self.assertEquals(ChromaticNote(12).get_name_up_to_octave(), "C")
        self.assertEquals(ChromaticNote(13).get_name_up_to_octave(), "C#")
        self.assertEquals(ChromaticNote(14).get_name_up_to_octave(), "D")
        self.assertEquals(ChromaticNote(-1).get_name_up_to_octave(), "B")
        self.assertEquals(ChromaticNote(-2).get_name_up_to_octave(), "B♭")
        self.assertEquals(ChromaticNote(-3).get_name_up_to_octave(), "A")
        self.assertEquals(ChromaticNote(-4).get_name_up_to_octave(), "A♭")
        self.assertEquals(ChromaticNote(-5).get_name_up_to_octave(), "G")
        self.assertEquals(ChromaticNote(-6).get_name_up_to_octave(), "F#")
        self.assertEquals(ChromaticNote(-7).get_name_up_to_octave(), "F")
        self.assertEquals(ChromaticNote(-8).get_name_up_to_octave(), "E")
        self.assertEquals(ChromaticNote(-9).get_name_up_to_octave(), "E♭")
        self.assertEquals(ChromaticNote(-10).get_name_up_to_octave(), "D")
        self.assertEquals(ChromaticNote(-11).get_name_up_to_octave(), "C#")
        self.assertEquals(ChromaticNote(-12).get_name_up_to_octave(), "C")
        self.assertEquals(ChromaticNote(-13).get_name_up_to_octave(), "B")
        self.assertEquals(ChromaticNote(-14).get_name_up_to_octave(), "B♭")

    def test_get_name_with_octave(self):
        self.assertEquals(ChromaticNote(0).get_full_name(), "C4")
        self.assertEquals(ChromaticNote(1).get_full_name(), "C#4")
        self.assertEquals(ChromaticNote(2).get_full_name(), "D4")
        self.assertEquals(ChromaticNote(3).get_full_name(), "E♭4")
        self.assertEquals(ChromaticNote(4).get_full_name(), "E4")
        self.assertEquals(ChromaticNote(5).get_full_name(), "F4")
        self.assertEquals(ChromaticNote(6).get_full_name(), "F#4")
        self.assertEquals(ChromaticNote(7).get_full_name(), "G4")
        self.assertEquals(ChromaticNote(8).get_full_name(), "A♭4")
        self.assertEquals(ChromaticNote(9).get_full_name(), "A4")
        self.assertEquals(ChromaticNote(10).get_full_name(), "B♭4")
        self.assertEquals(ChromaticNote(11).get_full_name(), "B4")
        self.assertEquals(ChromaticNote(12).get_full_name(), "C5")
        self.assertEquals(ChromaticNote(13).get_full_name(), "C#5")
        self.assertEquals(ChromaticNote(14).get_full_name(), "D5")
        self.assertEquals(ChromaticNote(-1).get_full_name(), "B3")
        self.assertEquals(ChromaticNote(-2).get_full_name(), "B♭3")
        self.assertEquals(ChromaticNote(-3).get_full_name(), "A3")
        self.assertEquals(ChromaticNote(-4).get_full_name(), "A♭3")
        self.assertEquals(ChromaticNote(-5).get_full_name(), "G3")
        self.assertEquals(ChromaticNote(-6).get_full_name(), "F#3")
        self.assertEquals(ChromaticNote(-7).get_full_name(), "F3")
        self.assertEquals(ChromaticNote(-8).get_full_name(), "E3")
        self.assertEquals(ChromaticNote(-9).get_full_name(), "E♭3")
        self.assertEquals(ChromaticNote(-10).get_full_name(), "D3")
        self.assertEquals(ChromaticNote(-11).get_full_name(), "C#3")
        self.assertEquals(ChromaticNote(-12).get_full_name(), "C3")
        self.assertEquals(ChromaticNote(-13).get_full_name(), "B2")
        self.assertEquals(ChromaticNote(-14).get_full_name(), "B♭2")

    def test_get_solfege(self):
        from solfege.note.note import Note
        self.assertEquals(ChromaticNote(0).get_solfege(), Note(chromatic=0, diatonic=0))
        self.assertEquals(ChromaticNote(1).get_solfege(), Note(chromatic=1, diatonic=0))
        self.assertEquals(ChromaticNote(2).get_solfege(), Note(chromatic=2, diatonic=1))
        self.assertEquals(ChromaticNote(3).get_solfege(), Note(chromatic=3, diatonic=2))
        self.assertEquals(ChromaticNote(4).get_solfege(), Note(chromatic=4, diatonic=2))
        self.assertEquals(ChromaticNote(5).get_solfege(), Note(chromatic=5, diatonic=3))
        self.assertEquals(ChromaticNote(6).get_solfege(), Note(chromatic=6, diatonic=3))
        self.assertEquals(ChromaticNote(7).get_solfege(), Note(chromatic=7, diatonic=4))
        self.assertEquals(ChromaticNote(8).get_solfege(), Note(chromatic=8, diatonic=5))
        self.assertEquals(ChromaticNote(9).get_solfege(), Note(chromatic=9, diatonic=5))
        self.assertEquals(ChromaticNote(10).get_solfege(), Note(chromatic=10, diatonic=6))
        self.assertEquals(ChromaticNote(11).get_solfege(), Note(chromatic=11, diatonic=6))
        self.assertEquals(ChromaticNote(12).get_solfege(), Note(chromatic=12, diatonic=7))
        self.assertEquals(ChromaticNote(13).get_solfege(), Note(chromatic=13, diatonic=7))
        self.assertEquals(ChromaticNote(14).get_solfege(), Note(chromatic=14, diatonic=8))
        self.assertEquals(ChromaticNote(-1).get_solfege(), Note(chromatic=-1, diatonic=-1))
        self.assertEquals(ChromaticNote(-2).get_solfege(), Note(chromatic=-2, diatonic=-1))
        self.assertEquals(ChromaticNote(-3).get_solfege(), Note(chromatic=-3, diatonic=-2))
        self.assertEquals(ChromaticNote(-4).get_solfege(), Note(chromatic=-4, diatonic=-2))
        self.assertEquals(ChromaticNote(-5).get_solfege(), Note(chromatic=-5, diatonic=-3))
        self.assertEquals(ChromaticNote(-6).get_solfege(), Note(chromatic=-6, diatonic=-4))
        self.assertEquals(ChromaticNote(-7).get_solfege(), Note(chromatic=-7, diatonic=-4))
        self.assertEquals(ChromaticNote(-8).get_solfege(), Note(chromatic=-8, diatonic=-5))
        self.assertEquals(ChromaticNote(-9).get_solfege(), Note(chromatic=-9, diatonic=-5))
        self.assertEquals(ChromaticNote(-10).get_solfege(), Note(chromatic=-10, diatonic=-6))
        self.assertEquals(ChromaticNote(-11).get_solfege(), Note(chromatic=-11, diatonic=-7))
        self.assertEquals(ChromaticNote(-12).get_solfege(), Note(chromatic=-12, diatonic=-7))
        self.assertEquals(ChromaticNote(-13).get_solfege(), Note(chromatic=-13, diatonic=-8))
        self.assertEquals(ChromaticNote(-14).get_solfege(), Note(chromatic=-14, diatonic=-8))

    def test_mul(self):
        with self.assertRaises(Exception):
            _ = self.D4 * 4
