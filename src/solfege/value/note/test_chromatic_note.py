from solfege.value.interval.chromatic_interval import ChromaticInterval
from solfege.value.interval.interval import Interval
from solfege.value.interval.test_chromatic_interval import TestChromaticInterval
from solfege.value.note.abstract_note import OctaveOutput
from solfege.value.note.diatonic_note import DiatonicNote
from solfege.value.note.note import Note
from solfege.value.note.chromatic_note import *

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
        """Restore `ChromaticNote`'s cross-class links, which other tests may have overwritten."""
        super().setUp()
        from solfege.value.note.diatonic_note import DiatonicNote
        from solfege.value.note.note import Note
        from solfege.value.note.note_alteration import NoteAlteration
        ChromaticNote.DiatonicClass = DiatonicNote
        ChromaticNote.PairClass = Note
        ChromaticNote.AlterationClass = NoteAlteration

    def test_classes(self):
        """`ChromaticNote`'s class-level links (interval/chromatic/pair/diatonic classes) point
        to the expected classes."""
        self.assertEqual(ChromaticNote.IntervalClass, ChromaticInterval)
        self.assertEqual(ChromaticNote.ChromaticClass, ChromaticNote)
        self.assertEqual(ChromaticNote.make_instance_of_selfs_class(0), ChromaticNote(0))
        self.assertEqual(ChromaticNote.PairClass, Note)
        self.assertEqual(ChromaticNote.DiatonicClass, DiatonicNote)

    # def test_is_note(self):
    #     self.assertTrue(self.C4.is_note())

    def test_get_number(self):
        """The `value` attribute exposes the raw chromatic (half-tone) position."""
        self.assertEqual(self.C4.value, 0)

    def test_equal(self):
        """Equality compares by chromatic value."""
        self.assertEqual(self.C4, self.C4)
        self.assertNotEqual(self.D4, self.C4)
        self.assertEqual(self.D4, self.D4)

    def test_add(self):
        """Adding a `ChromaticInterval` to a note (either order) shifts it; adding two notes fails."""
        self.assertEqual(self.D4 + self.third_minor, self.F4)
        self.assertEqual(self.third_minor + self.D4, self.F4)
        # self.assertEqual(self.D4 + Interval.make(3, 2), self.F4)
        # self.assertEqual(Interval.make(3, 2) + self.D4, self.F4)
        with self.assertRaises(Exception):
            _ = self.D4 + self.D4

    def test_neg(self):
        """Negating a note is not supported."""
        with self.assertRaises(Exception):
            _ = -self.D4

    def test_sub(self):
        """Subtracting an interval shifts the note; subtracting a note yields an interval; a note
        cannot be subtracted from an interval."""
        self.assertEqual(self.F4 - self.third_minor, self.D4)
        self.assertEqual(self.F4 - self.D4, self.third_minor)
        with self.assertRaises(Exception):
            _ = self.third_minor - self.D4

    def test_lt(self):
        """Notes order by chromatic value."""
        self.assertLess(self.D4, self.F4)
        self.assertLessEqual(self.D4, self.F4)
        self.assertLessEqual(self.D4, self.D4)

    def test_repr(self):
        """`repr` shows the constructor call that would rebuild the note."""
        self.assertEqual(repr(self.D4), "ChromaticNote(value=2)")

    def test_octave(self):
        """`octave` returns the octave index (0 for the octave containing middle C)."""
        self.assertEqual(self.C4.octave(), 0)
        self.assertEqual(self.B4.octave(), 0)
        self.assertEqual(self.D3.octave(), -1)
        self.assertEqual(self.C3.octave(), -1)
        self.assertEqual(self.B2.octave(), -2)
        self.assertEqual(self.C5.octave(), 1)

    def test_add_octave(self):
        """`add_octave` shifts a note by whole octaves."""
        self.assertEqual(self.C5.add_octave(-1), self.C4)
        self.assertEqual(self.C4.add_octave(1), self.C5)
        self.assertEqual(self.C5.add_octave(-2), self.C3)
        self.assertEqual(self.C3.add_octave(2), self.C5)

    def test_same_note_in_base_octave(self):
        """`in_base_octave` folds a note into the reference octave, keeping diatonic-letter
        identity (e.g. B3 folds to B4, not C4)."""
        self.assertEqual(self.C5.in_base_octave(), self.C4)
        self.assertEqual(self.C3.in_base_octave(), self.C4)
        self.assertEqual(self.C4.in_base_octave(), self.C4)
        self.assertEqual(self.D4.in_base_octave(), self.D4)
        self.assertEqual(self.B3.in_base_octave(), self.B4)

    def test_same_note_in_different_octaves(self):
        """`equals_modulo_octave` is true only for the same pitch class across octaves."""
        self.assertFalse(self.D4.equals_modulo_octave(self.C4))
        self.assertFalse(self.D4.equals_modulo_octave(self.C5))
        self.assertFalse(self.D4.equals_modulo_octave(self.C3))
        self.assertFalse(self.D4.equals_modulo_octave(self.B3))
        self.assertTrue(self.C4.equals_modulo_octave(self.C4))
        self.assertTrue(self.C4.equals_modulo_octave(self.C5))
        self.assertTrue(self.C4.equals_modulo_octave(self.C3))
        self.assertTrue(self.C5.equals_modulo_octave(self.C3))

    def test_get_interval_name(self):
        """`get_name_up_to_octave` spells every chromatic value (0-14 and -1..-14) as a letter
        name with symbol alteration, using sharps ascending and flats descending."""
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
        """`get_name_with_octave` appends the scientific-notation octave number to the note
        name, across a two-octave range."""
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

    # def test_get_pair(self):
    #     from solfege.value.note.note import Note
    #     self.assertEqual(ChromaticNote(0).get_pair(), Note.make(0, 0))
    #     self.assertEqual(ChromaticNote(1).get_pair(), Note.make(1, 0))
    #     self.assertEqual(ChromaticNote(2).get_pair(), Note.make(2, 1))
    #     self.assertEqual(ChromaticNote(3).get_pair(), Note.make(3, 2))
    #     self.assertEqual(ChromaticNote(4).get_pair(), Note.make(4, 2))
    #     self.assertEqual(ChromaticNote(5).get_pair(), Note.make(5, 3))
    #     self.assertEqual(ChromaticNote(6).get_pair(), Note.make(6, 3))
    #     self.assertEqual(ChromaticNote(7).get_pair(), Note.make(7, 4))
    #     self.assertEqual(ChromaticNote(8).get_pair(), Note.make(8, 5))
    #     self.assertEqual(ChromaticNote(9).get_pair(), Note.make(9, 5))
    #     self.assertEqual(ChromaticNote(10).get_pair(), Note.make(10, 6))
    #     self.assertEqual(ChromaticNote(11).get_pair(), Note.make(11, 6))
    #     self.assertEqual(ChromaticNote(12).get_pair(), Note.make(12, 7))
    #     self.assertEqual(ChromaticNote(13).get_pair(), Note.make(13, 7))
    #     self.assertEqual(ChromaticNote(14).get_pair(), Note.make(14, 8))
    #     self.assertEqual(ChromaticNote(-1).get_pair(), Note.make(-1, -1))
    #     self.assertEqual(ChromaticNote(-2).get_pair(), Note.make(-2, -1))
    #     self.assertEqual(ChromaticNote(-3).get_pair(), Note.make(-3, -2))
    #     self.assertEqual(ChromaticNote(-4).get_pair(), Note.make(-4, -2))
    #     self.assertEqual(ChromaticNote(-5).get_pair(), Note.make(-5, -3))
    #     self.assertEqual(ChromaticNote(-6).get_pair(), Note.make(-6, -4))
    #     self.assertEqual(ChromaticNote(-7).get_pair(), Note.make(-7, -4))
    #     self.assertEqual(ChromaticNote(-8).get_pair(), Note.make(-8, -5))
    #     self.assertEqual(ChromaticNote(-9).get_pair(), Note.make(-9, -5))
    #     self.assertEqual(ChromaticNote(-10).get_pair(), Note.make(-10, -6))
    #     self.assertEqual(ChromaticNote(-11).get_pair(), Note.make(-11, -7))
    #     self.assertEqual(ChromaticNote(-12).get_pair(), Note.make(-12, -7))
    #     self.assertEqual(ChromaticNote(-13).get_pair(), Note.make(-13, -8))
    #     self.assertEqual(ChromaticNote(-14).get_pair(), Note.make(-14, -8))

    def test_mul(self):
        """Multiplying a note by a scalar is not supported."""
        with self.assertRaises(Exception):
            _ = self.D4 * 4
