from solfege.interval.test_chromatic import TestChromaticInterval
from solfege.note.abstract import OctaveOutput
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
        self.assertEqual(self.C4.get_number(), 0)

    def test_equal(self):
        self.assertEqual(self.C4, self.C4)
        self.assertNotEqual(self.D4, self.C4)
        self.assertEqual(self.D4, self.D4)

    def test_add(self):
        self.assertEqual(self.D4 + self.third_minor, self.F4)
        self.assertEqual(self.third_minor + self.D4, self.F4)
        with self.assertRaises(Exception):
            _ = self.D4 + self.D4

    def test_neg(self):
        with self.assertRaises(Exception):
            _ = -self.D4

    def test_sub(self):
        self.assertEqual(self.F4 - self.third_minor, self.D4)
        self.assertEqual(self.F4 - self.D4, self.third_minor)
        with self.assertRaises(Exception):
            _ = self.third_minor - self.D4

    def test_lt(self):
        self.assertLess(self.D4, self.F4)
        self.assertLessEqual(self.D4, self.F4)
        self.assertLessEqual(self.D4, self.D4)

    def test_repr(self):
        self.assertEqual(repr(self.D4), "ChromaticNote(value=2)")

    def test_get_octave(self):
        self.assertEqual(self.C4.get_octave(), 0)
        self.assertEqual(self.B4.get_octave(), 0)
        self.assertEqual(self.D3.get_octave(), -1)
        self.assertEqual(self.C3.get_octave(), -1)
        self.assertEqual(self.B2.get_octave(), -2)
        self.assertEqual(self.C5.get_octave(), 1)

    def test_add_octave(self):
        self.assertEqual(self.C5.add_octave(-1), self.C4)
        self.assertEqual(self.C4.add_octave(1), self.C5)
        self.assertEqual(self.C5.add_octave(-2), self.C3)
        self.assertEqual(self.C3.add_octave(2), self.C5)

    def test_same_note_in_base_octave(self):
        self.assertEqual(self.C5.get_in_base_octave(), self.C4)
        self.assertEqual(self.C3.get_in_base_octave(), self.C4)
        self.assertEqual(self.C4.get_in_base_octave(), self.C4)
        self.assertEqual(self.D4.get_in_base_octave(), self.D4)
        self.assertEqual(self.B3.get_in_base_octave(), self.B4)

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
        self.assertEqual(ChromaticNote(0).get_name_up_to_octave(note_output=NoteOutput.LETTER, alteration_output=AlterationOutput.SYMBOL, fixed_length=FixedLengthOutput.NO), "C")
        self.assertEqual(ChromaticNote(1).get_name_up_to_octave(note_output=NoteOutput.LETTER, alteration_output=AlterationOutput.SYMBOL, fixed_length=FixedLengthOutput.NO), "C#")
        self.assertEqual(ChromaticNote(2).get_name_up_to_octave(note_output=NoteOutput.LETTER, alteration_output=AlterationOutput.SYMBOL, fixed_length=FixedLengthOutput.NO), "D")
        self.assertEqual(ChromaticNote(3).get_name_up_to_octave(note_output=NoteOutput.LETTER, alteration_output=AlterationOutput.SYMBOL, fixed_length=FixedLengthOutput.NO), "E♭")
        self.assertEqual(ChromaticNote(4).get_name_up_to_octave(note_output=NoteOutput.LETTER, alteration_output=AlterationOutput.SYMBOL, fixed_length=FixedLengthOutput.NO), "E")
        self.assertEqual(ChromaticNote(5).get_name_up_to_octave(note_output=NoteOutput.LETTER, alteration_output=AlterationOutput.SYMBOL, fixed_length=FixedLengthOutput.NO), "F")
        self.assertEqual(ChromaticNote(6).get_name_up_to_octave(note_output=NoteOutput.LETTER, alteration_output=AlterationOutput.SYMBOL, fixed_length=FixedLengthOutput.NO), "F#")
        self.assertEqual(ChromaticNote(7).get_name_up_to_octave(note_output=NoteOutput.LETTER, alteration_output=AlterationOutput.SYMBOL, fixed_length=FixedLengthOutput.NO), "G")
        self.assertEqual(ChromaticNote(8).get_name_up_to_octave(note_output=NoteOutput.LETTER, alteration_output=AlterationOutput.SYMBOL, fixed_length=FixedLengthOutput.NO), "A♭")
        self.assertEqual(ChromaticNote(9).get_name_up_to_octave(note_output=NoteOutput.LETTER, alteration_output=AlterationOutput.SYMBOL, fixed_length=FixedLengthOutput.NO), "A")
        self.assertEqual(ChromaticNote(10).get_name_up_to_octave(note_output=NoteOutput.LETTER, alteration_output=AlterationOutput.SYMBOL, fixed_length=FixedLengthOutput.NO), "B♭")
        self.assertEqual(ChromaticNote(11).get_name_up_to_octave(note_output=NoteOutput.LETTER, alteration_output=AlterationOutput.SYMBOL, fixed_length=FixedLengthOutput.NO), "B")
        self.assertEqual(ChromaticNote(12).get_name_up_to_octave(note_output=NoteOutput.LETTER, alteration_output=AlterationOutput.SYMBOL, fixed_length=FixedLengthOutput.NO), "C")
        self.assertEqual(ChromaticNote(13).get_name_up_to_octave(note_output=NoteOutput.LETTER, alteration_output=AlterationOutput.SYMBOL, fixed_length=FixedLengthOutput.NO), "C#")
        self.assertEqual(ChromaticNote(14).get_name_up_to_octave(note_output=NoteOutput.LETTER, alteration_output=AlterationOutput.SYMBOL, fixed_length=FixedLengthOutput.NO), "D")
        self.assertEqual(ChromaticNote(-1).get_name_up_to_octave(note_output=NoteOutput.LETTER, alteration_output=AlterationOutput.SYMBOL, fixed_length=FixedLengthOutput.NO), "B")
        self.assertEqual(ChromaticNote(-2).get_name_up_to_octave(note_output=NoteOutput.LETTER, alteration_output=AlterationOutput.SYMBOL, fixed_length=FixedLengthOutput.NO), "B♭")
        self.assertEqual(ChromaticNote(-3).get_name_up_to_octave(note_output=NoteOutput.LETTER, alteration_output=AlterationOutput.SYMBOL, fixed_length=FixedLengthOutput.NO), "A")
        self.assertEqual(ChromaticNote(-4).get_name_up_to_octave(note_output=NoteOutput.LETTER, alteration_output=AlterationOutput.SYMBOL, fixed_length=FixedLengthOutput.NO), "A♭")
        self.assertEqual(ChromaticNote(-5).get_name_up_to_octave(note_output=NoteOutput.LETTER, alteration_output=AlterationOutput.SYMBOL, fixed_length=FixedLengthOutput.NO), "G")
        self.assertEqual(ChromaticNote(-6).get_name_up_to_octave(note_output=NoteOutput.LETTER, alteration_output=AlterationOutput.SYMBOL, fixed_length=FixedLengthOutput.NO), "F#")
        self.assertEqual(ChromaticNote(-7).get_name_up_to_octave(note_output=NoteOutput.LETTER, alteration_output=AlterationOutput.SYMBOL, fixed_length=FixedLengthOutput.NO), "F")
        self.assertEqual(ChromaticNote(-8).get_name_up_to_octave(note_output=NoteOutput.LETTER, alteration_output=AlterationOutput.SYMBOL, fixed_length=FixedLengthOutput.NO), "E")
        self.assertEqual(ChromaticNote(-9).get_name_up_to_octave(note_output=NoteOutput.LETTER, alteration_output=AlterationOutput.SYMBOL, fixed_length=FixedLengthOutput.NO), "E♭")
        self.assertEqual(ChromaticNote(-10).get_name_up_to_octave(note_output=NoteOutput.LETTER, alteration_output=AlterationOutput.SYMBOL, fixed_length=FixedLengthOutput.NO), "D")
        self.assertEqual(ChromaticNote(-11).get_name_up_to_octave(note_output=NoteOutput.LETTER, alteration_output=AlterationOutput.SYMBOL, fixed_length=FixedLengthOutput.NO), "C#")
        self.assertEqual(ChromaticNote(-12).get_name_up_to_octave(note_output=NoteOutput.LETTER, alteration_output=AlterationOutput.SYMBOL, fixed_length=FixedLengthOutput.NO), "C")
        self.assertEqual(ChromaticNote(-13).get_name_up_to_octave(note_output=NoteOutput.LETTER, alteration_output=AlterationOutput.SYMBOL, fixed_length=FixedLengthOutput.NO), "B")
        self.assertEqual(ChromaticNote(-14).get_name_up_to_octave(note_output=NoteOutput.LETTER, alteration_output=AlterationOutput.SYMBOL, fixed_length=FixedLengthOutput.NO), "B♭")

    def test_get_name_with_octave(self):
        self.assertEqual(ChromaticNote(0).get_name_with_octave(octave_notation=OctaveOutput.MIDDLE_IS_4, alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "C4")
        self.assertEqual(ChromaticNote(1).get_name_with_octave(octave_notation=OctaveOutput.MIDDLE_IS_4, alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "C#4")
        self.assertEqual(ChromaticNote(2).get_name_with_octave(octave_notation=OctaveOutput.MIDDLE_IS_4, alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "D4")
        self.assertEqual(ChromaticNote(3).get_name_with_octave(octave_notation=OctaveOutput.MIDDLE_IS_4, alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "E♭4")
        self.assertEqual(ChromaticNote(4).get_name_with_octave(octave_notation=OctaveOutput.MIDDLE_IS_4, alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "E4")
        self.assertEqual(ChromaticNote(5).get_name_with_octave(octave_notation=OctaveOutput.MIDDLE_IS_4, alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "F4")
        self.assertEqual(ChromaticNote(6).get_name_with_octave(octave_notation=OctaveOutput.MIDDLE_IS_4, alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "F#4")
        self.assertEqual(ChromaticNote(7).get_name_with_octave(octave_notation=OctaveOutput.MIDDLE_IS_4, alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "G4")
        self.assertEqual(ChromaticNote(8).get_name_with_octave(octave_notation=OctaveOutput.MIDDLE_IS_4, alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "A♭4")
        self.assertEqual(ChromaticNote(9).get_name_with_octave(octave_notation=OctaveOutput.MIDDLE_IS_4, alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "A4")
        self.assertEqual(ChromaticNote(10).get_name_with_octave(octave_notation=OctaveOutput.MIDDLE_IS_4, alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "B♭4")
        self.assertEqual(ChromaticNote(11).get_name_with_octave(octave_notation=OctaveOutput.MIDDLE_IS_4, alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "B4")
        self.assertEqual(ChromaticNote(12).get_name_with_octave(octave_notation=OctaveOutput.MIDDLE_IS_4, alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "C5")
        self.assertEqual(ChromaticNote(13).get_name_with_octave(octave_notation=OctaveOutput.MIDDLE_IS_4, alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "C#5")
        self.assertEqual(ChromaticNote(14).get_name_with_octave(octave_notation=OctaveOutput.MIDDLE_IS_4, alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "D5")
        self.assertEqual(ChromaticNote(-1).get_name_with_octave(octave_notation=OctaveOutput.MIDDLE_IS_4, alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "B3")
        self.assertEqual(ChromaticNote(-2).get_name_with_octave(octave_notation=OctaveOutput.MIDDLE_IS_4, alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "B♭3")
        self.assertEqual(ChromaticNote(-3).get_name_with_octave(octave_notation=OctaveOutput.MIDDLE_IS_4, alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "A3")
        self.assertEqual(ChromaticNote(-4).get_name_with_octave(octave_notation=OctaveOutput.MIDDLE_IS_4, alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "A♭3")
        self.assertEqual(ChromaticNote(-5).get_name_with_octave(octave_notation=OctaveOutput.MIDDLE_IS_4, alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "G3")
        self.assertEqual(ChromaticNote(-6).get_name_with_octave(octave_notation=OctaveOutput.MIDDLE_IS_4, alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "F#3")
        self.assertEqual(ChromaticNote(-7).get_name_with_octave(octave_notation=OctaveOutput.MIDDLE_IS_4, alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "F3")
        self.assertEqual(ChromaticNote(-8).get_name_with_octave(octave_notation=OctaveOutput.MIDDLE_IS_4, alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "E3")
        self.assertEqual(ChromaticNote(-9).get_name_with_octave(octave_notation=OctaveOutput.MIDDLE_IS_4, alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "E♭3")
        self.assertEqual(ChromaticNote(-10).get_name_with_octave(octave_notation=OctaveOutput.MIDDLE_IS_4, alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "D3")
        self.assertEqual(ChromaticNote(-11).get_name_with_octave(octave_notation=OctaveOutput.MIDDLE_IS_4, alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "C#3")
        self.assertEqual(ChromaticNote(-12).get_name_with_octave(octave_notation=OctaveOutput.MIDDLE_IS_4, alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "C3")
        self.assertEqual(ChromaticNote(-13).get_name_with_octave(octave_notation=OctaveOutput.MIDDLE_IS_4, alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "B2")
        self.assertEqual(ChromaticNote(-14).get_name_with_octave(octave_notation=OctaveOutput.MIDDLE_IS_4, alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "B♭2")

    def test_get_solfege(self):
        from solfege.note.note import Note
        self.assertEqual(ChromaticNote(0).get_solfege(), Note(chromatic=0, diatonic=0))
        self.assertEqual(ChromaticNote(1).get_solfege(), Note(chromatic=1, diatonic=0))
        self.assertEqual(ChromaticNote(2).get_solfege(), Note(chromatic=2, diatonic=1))
        self.assertEqual(ChromaticNote(3).get_solfege(), Note(chromatic=3, diatonic=2))
        self.assertEqual(ChromaticNote(4).get_solfege(), Note(chromatic=4, diatonic=2))
        self.assertEqual(ChromaticNote(5).get_solfege(), Note(chromatic=5, diatonic=3))
        self.assertEqual(ChromaticNote(6).get_solfege(), Note(chromatic=6, diatonic=3))
        self.assertEqual(ChromaticNote(7).get_solfege(), Note(chromatic=7, diatonic=4))
        self.assertEqual(ChromaticNote(8).get_solfege(), Note(chromatic=8, diatonic=5))
        self.assertEqual(ChromaticNote(9).get_solfege(), Note(chromatic=9, diatonic=5))
        self.assertEqual(ChromaticNote(10).get_solfege(), Note(chromatic=10, diatonic=6))
        self.assertEqual(ChromaticNote(11).get_solfege(), Note(chromatic=11, diatonic=6))
        self.assertEqual(ChromaticNote(12).get_solfege(), Note(chromatic=12, diatonic=7))
        self.assertEqual(ChromaticNote(13).get_solfege(), Note(chromatic=13, diatonic=7))
        self.assertEqual(ChromaticNote(14).get_solfege(), Note(chromatic=14, diatonic=8))
        self.assertEqual(ChromaticNote(-1).get_solfege(), Note(chromatic=-1, diatonic=-1))
        self.assertEqual(ChromaticNote(-2).get_solfege(), Note(chromatic=-2, diatonic=-1))
        self.assertEqual(ChromaticNote(-3).get_solfege(), Note(chromatic=-3, diatonic=-2))
        self.assertEqual(ChromaticNote(-4).get_solfege(), Note(chromatic=-4, diatonic=-2))
        self.assertEqual(ChromaticNote(-5).get_solfege(), Note(chromatic=-5, diatonic=-3))
        self.assertEqual(ChromaticNote(-6).get_solfege(), Note(chromatic=-6, diatonic=-4))
        self.assertEqual(ChromaticNote(-7).get_solfege(), Note(chromatic=-7, diatonic=-4))
        self.assertEqual(ChromaticNote(-8).get_solfege(), Note(chromatic=-8, diatonic=-5))
        self.assertEqual(ChromaticNote(-9).get_solfege(), Note(chromatic=-9, diatonic=-5))
        self.assertEqual(ChromaticNote(-10).get_solfege(), Note(chromatic=-10, diatonic=-6))
        self.assertEqual(ChromaticNote(-11).get_solfege(), Note(chromatic=-11, diatonic=-7))
        self.assertEqual(ChromaticNote(-12).get_solfege(), Note(chromatic=-12, diatonic=-7))
        self.assertEqual(ChromaticNote(-13).get_solfege(), Note(chromatic=-13, diatonic=-8))
        self.assertEqual(ChromaticNote(-14).get_solfege(), Note(chromatic=-14, diatonic=-8))

    def test_mul(self):
        with self.assertRaises(Exception):
            _ = self.D4 * 4
