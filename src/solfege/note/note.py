from solfege.interval.interval import Interval, TestChromaticInterval
from solfege.note import ChromaticNote, DiatonicNote


class Note(Interval, ChromaticNote):
    IntervalClass = Interval
    DiatonicClass = DiatonicNote
    ChromaticClass = ChromaticNote
    """A note of the scale, as an interval from middle C."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __neg__(self):
        raise Exception("Trying to negate a note makes no sens.")

    def sub_note(self, other):
        diatonic = self.get_diatonic() - other.get_diatonic()
        chromatic = self.get_chromatic().__sub__(other)

        return Interval(
            diatonic=diatonic.get_number(),
            chromatic=chromatic.get_number()
        )

    def get_interval_name(self, forFile=None):
        """The name of this note.

        Args: `forFile` -- whether we should avoid non ascii symbol"""
        diatonic = self.get_diatonic()
        try:
            alteration = self.get_alteration()
        except TooBigAlteration as tba:
            tba.addInformation("Note", self)
            raise
        return f"{diatonic.get_interval_name().upper()}{alteration.get_interval_name(forFile=forFile)}"

    def correctAlteration(self):
        """Whether the note has a printable alteration."""
        return self.get_alteration().printable()


class TestChromaticNote(TestChromaticInterval):
    C3 = Note(chromatic=-12, diatonic=-7)
    B3 = Note(chromatic=-1, diatonic=-1)
    C4 = Note(chromatic=0, diatonic=0)
    C4_sharp = Note(chromatic=1, diatonic=1)
    D4 = Note(chromatic=2, diatonic=1)
    E4b = Note(chromatic=3, diatonic=2)
    F4 = Note(chromatic=5, diatonic=3)
    C5 = Note(chromatic=12, diatonic=7)

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
        self.assertEquals(self.D4 + self.third_minor, self.F4)
        sum_ = self.third_minor + self.D4
        self.assertEquals(sum_, self.F4)

    def test_neg(self):
        with self.assertRaises(Exception):
            _ = -self.D4

    def test_sub(self):
        self.assertEquals(self.F4 - self.D4, self.third_minor)
        self.assertEquals(self.F4 - self.third_minor, self.D4)
        with self.assertRaises(Exception):
            _ = self.third_minor - self.C4

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
        self.assertEquals(self.C5.get_same_note_in_base_octave(), self.C4)
        self.assertEquals(self.C3.get_same_note_in_base_octave(), self.C4)
        self.assertEquals(self.C4.get_same_note_in_base_octave(), self.C4)
        self.assertEquals(self.D4.get_same_note_in_base_octave(), self.D4)

    def test_same_note_in_different_octaves(self):
        self.assertFalse(self.D4.same_notes_in_different_octaves(self.C4))
        self.assertFalse(self.D4.same_notes_in_different_octaves(self.C5))
        self.assertFalse(self.D4.same_notes_in_different_octaves(self.C3))
        self.assertTrue(self.C4.same_notes_in_different_octaves(self.C4))
        self.assertTrue(self.C4.same_notes_in_different_octaves(self.C5))
        self.assertTrue(self.C4.same_notes_in_different_octaves(self.C3))
        self.assertTrue(self.C5.same_notes_in_different_octaves(self.C3))
