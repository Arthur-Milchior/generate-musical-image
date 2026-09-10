import unittest

from solfege.value.note.abstract_note import OctaveOutput
from solfege.value.note.note import *
from solfege.value.interval.interval import *

class TestNote(unittest.TestCase):
    C3 = Note.make(-12, -7)
    B3 = Note.make(-1, -1)
    A3 = Note.make(-3, -2)
    B3_flat = Note.make(-2, -1)
    C4 = Note.make(0, 0)
    C4_sharp = Note.make(1, 1)
    D4 = Note.make(2, 1)
    D4_sharp = Note.make(3, 1)
    E4b = Note.make(3, 2)
    E4 = Note.make(4, 2)
    F4 = Note.make(5, 3)
    C5 = Note.make(12, 7)

    def test_all_from_chromatic(self) -> None:
        """`all_from_chromatic` returns every diatonic spelling of a chromatic value, natural
        spelling first."""
        self.assertEqual(Note.all_from_chromatic(ChromaticNote(0)), [Note.make(0, 0), Note.make(0, -1), Note.make(0, 1)])
        self.assertEqual(Note.all_from_chromatic(ChromaticNote(11)), [Note.make(11, 6), Note.make(11, 7), Note.make(11, 5)])
        self.assertEqual(Note.all_from_chromatic(ChromaticNote(4)), [Note.make(4, 2), Note.make(4, 3), Note.make(4, 1)])

    def test_lily(self) -> None:
        """`syntax_for_lily` renders the LilyPond note name including octave marks."""
        self.assertEqual(self.C4.syntax_for_lily(), "c'")
        self.assertEqual(self.F4.syntax_for_lily(), "f'")

    # def test_is_note(self):
    #     self.assertTrue(self.C4.is_note())

    def test_equal(self) -> None:
        """Equality compares by chromatic+diatonic value pair."""
        self.assertEqual(self.C4, self.C4)
        self.assertNotEqual(self.D4, self.C4)
        self.assertEqual(self.D4, self.D4)

    def test_add(self) -> None:
        """Adding an `Interval` to a note (either order) shifts it; adding two notes fails."""
        with self.assertRaises(Exception):
            _ = self.D4 + self.C4
        self.assertEqual(self.D4 + third_minor, self.F4)
        self.assertEqual(third_minor + self.D4, self.F4)
        # self.assertEqual(self.D4 + ChromaticInterval.make(1), ChromaticNote(3))
        # self.assertEqual(ChromaticInterval.make(1) + self.D4, ChromaticNote(3))
        # self.assertEqual(self.D4 + DiatonicInterval.make(1), DiatonicNote(2))
        # self.assertEqual(DiatonicInterval.make(1) + self.D4, DiatonicNote(2))

    def test_neg(self) -> None:
        """Negating a note is not supported."""
        with self.assertRaises(Exception):
            _ = -self.D4

    def test_sub(self) -> None:
        """Subtracting a note yields an interval; subtracting an interval shifts the note; an
        interval cannot be subtracted from a note the other way round."""
        self.assertEqual(self.F4 - self.D4, third_minor)
        self.assertEqual(self.F4 - third_minor, self.D4)
        with self.assertRaises(Exception):
            _ = third_minor - self.C4

    def test_lt(self) -> None:
        """Notes order by pitch."""
        self.assertLess(self.C4_sharp, self.D4)
        self.assertLessEqual(self.C4_sharp, self.D4)
        self.assertLessEqual(self.D4, self.D4)

    def test_repr(self) -> None:
        """`repr` shows the `Note.make(chromatic, diatonic)` call that would rebuild the note."""
        self.assertEqual(repr(self.D4), "Note.make(2, 1)")

    def test_octave(self) -> None:
        """`octave` returns the octave index (0 for the octave containing middle C)."""
        self.assertEqual(self.C4.octave(), 0)
        self.assertEqual(self.C3.octave(), -1)
        self.assertEqual(self.C5.octave(), 1)

    def test_add_octave(self) -> None:
        """`add_octave` shifts a note by whole octaves."""
        self.assertEqual(self.C5.add_octave(-1), self.C4)
        self.assertEqual(self.C4.add_octave(1), self.C5)
        self.assertEqual(self.C5.add_octave(-2), self.C3)
        self.assertEqual(self.C3.add_octave(2), self.C5)

    def test_same_note_in_base_octave(self) -> None:
        """`in_base_octave` folds a note into the reference octave."""
        self.assertEqual(self.C5.in_base_octave(), self.C4)
        self.assertEqual(self.C3.in_base_octave(), self.C4)
        self.assertEqual(self.C4.in_base_octave(), self.C4)
        self.assertEqual(self.D4.in_base_octave(), self.D4)

    def test_same_note_in_different_octaves(self) -> None:
        """`equals_modulo_octave` is true only for the same pitch across octaves."""
        self.assertFalse(self.D4.equals_modulo_octave(self.C4))
        self.assertFalse(self.D4.equals_modulo_octave(self.C5))
        self.assertFalse(self.D4.equals_modulo_octave(self.C3))
        self.assertTrue(self.C4.equals_modulo_octave(self.C4))
        self.assertTrue(self.C4.equals_modulo_octave(self.C5))
        self.assertTrue(self.C4.equals_modulo_octave(self.C3))
        self.assertTrue(self.C5.equals_modulo_octave(self.C3))

    def test_lily_black(self) -> None:
        """`syntax_for_lily` uses no mark for the reference octave and `'`/no-mark for
        octaves above/below (regression check for black-key-adjacent notes like B3)."""
        self.assertEqual(self.C4.syntax_for_lily(), "c'")
        self.assertEqual(self.C3.syntax_for_lily(), "c")
        self.assertEqual(self.C5.syntax_for_lily(), "c''")
        self.assertEqual(self.B3.syntax_for_lily(), "b")

    def test_is_black_key(self) -> None:
        """`is_black_key_on_piano` is true for sharped/flatted notes, false for naturals."""
        self.assertFalse(self.C4.is_black_key_on_piano())
        self.assertTrue(self.C4_sharp.is_black_key_on_piano())

    def test_adjacent(self) -> None:
        """`adjacent` is true for notes at most two half-tones apart, with an extra
        natural/enharmonic edge case around C and F, and raises when compared to itself."""
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

        self.assertFalse(Note.from_name("C4#").adjacent(Note.from_name("B3♭")))
        self.assertFalse(Note.from_name("D4").adjacent(Note.from_name("B3")))
        self.assertFalse(Note.from_name("F").adjacent(Note.from_name("D")))
        self.assertFalse(Note.from_name("F#").adjacent(Note.from_name("D#")))
        self.assertFalse(Note.from_name("G").adjacent(Note.from_name("E")))
        self.assertTrue(Note.from_name("D#").adjacent(Note.from_name("C")))
        self.assertTrue(Note.from_name("E").adjacent(Note.from_name("C#")))
        self.assertTrue(Note.from_name("G#").adjacent(Note.from_name("F")))
        self.assertTrue(Note.from_name("A").adjacent(Note.from_name("G♭")))
        self.assertTrue(Note.from_name("A#").adjacent(Note.from_name("G")))
        self.assertTrue(Note.from_name("B").adjacent(Note.from_name("A♭")))

    def test_from_name(self) -> None:
        """`from_name` parses a letter, optional alteration symbol (before or after the octave
        digit), and optional octave digit."""
        self.assertEqual(Note.from_name("C"), Note.make(0, 0))
        self.assertEqual(Note.from_name("C4"), Note.make(0, 0))
        self.assertEqual(Note.from_name("B3#"), Note.make(0, -1))
        self.assertEqual(Note.from_name("B#3"), Note.make(0, -1))

        self.assertEqual(Note.from_name("C♭"), Note.make(-1, 0))
        self.assertEqual(Note.from_name("C4♭"), Note.make(-1, 0))
        self.assertEqual(Note.from_name("C♭4"), Note.make(-1, 0))
        self.assertEqual(Note.from_name("B3"), Note.make(-1, -1))

    def test_from_name_to_name(self) -> None:
        """Round-tripping `from_name` through `get_name_with_octave` reproduces the input."""
        self.assertEqual(Note.from_name("C4").get_name_with_octave(octave_notation=OctaveOutput.MIDDLE_IS_4, alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO, ), "C4")
        self.assertEqual(Note.from_name("C♭4").get_name_with_octave(octave_notation=OctaveOutput.MIDDLE_IS_4, alteration_output=AlterationOutput.SYMBOL, note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO, ), "C♭4")

    def test_simplest_enharmonic(self) -> None:
        """`simplest_enharmonic` prefers no alteration, then falls back to a white-key-adjacent
        single sharp/flat, resolving double alterations first."""
        self.assertEqual(Note.from_name("C").simplest_enharmonic(), Note.from_name("C"))
        self.assertEqual(Note.from_name("C♭").simplest_enharmonic(), Note.from_name("B3"))
        self.assertEqual(Note.from_name("B3#").simplest_enharmonic(), Note.from_name("C"))
        self.assertEqual(Note.from_name("C#").simplest_enharmonic(), Note.from_name("C#"))
        self.assertEqual(Note.from_name("C##").simplest_enharmonic(), Note.from_name("D"))
        self.assertEqual(Note.from_name("D♭").simplest_enharmonic(), Note.from_name("D♭"))
        self.assertEqual(Note.from_name("D♭♭").simplest_enharmonic(), Note.from_name("C"))

    def test_canonize(self) -> None:
        """`canonize` picks a spelling with at most one alteration, preferring sharp when
        `for_sharp` is true and flat otherwise."""
        self.assertEqual(Note.from_name("C").canonize(for_sharp=True), Note.from_name("C"))
        self.assertEqual(Note.from_name("C♭").canonize(for_sharp=True), Note.from_name("B3"))
        self.assertEqual(Note.from_name("B3#").canonize(for_sharp=True), Note.from_name("C"))
        self.assertEqual(Note.from_name("C#").canonize(for_sharp=True), Note.from_name("C#"))
        self.assertEqual(Note.from_name("C##").canonize(for_sharp=True), Note.from_name("D"))
        self.assertEqual(Note.from_name("D♭").canonize(for_sharp=True), Note.from_name("C#"))
        self.assertEqual(Note.from_name("D♭♭").canonize(for_sharp=False), Note.from_name("C"))
        self.assertEqual(Note.from_name("C").canonize(for_sharp=False), Note.from_name("C"))
        self.assertEqual(Note.from_name("C♭").canonize(for_sharp=False), Note.from_name("B3"))
        self.assertEqual(Note.from_name("B3#").canonize(for_sharp=False), Note.from_name("C"))
        self.assertEqual(Note.from_name("C#").canonize(for_sharp=False), Note.from_name("D♭"))
        self.assertEqual(Note.from_name("C##").canonize(for_sharp=False), Note.from_name("D"))
        self.assertEqual(Note.from_name("D♭").canonize(for_sharp=False), Note.from_name("D♭"))
        self.assertEqual(Note.from_name("D♭♭").canonize(for_sharp=False), Note.from_name("C"))


    def test_change_octave(self) -> None:
        """`change_octave_to_be_enharmonic` shifts a note by whole octaves to match a given
        chromatic note."""
        c4 = Note.make(0, 0)
        self.assertEqual(c4.change_octave_to_be_enharmonic(ChromaticNote(12)), Note.make(12, 7))
    # todo Test wwith color
