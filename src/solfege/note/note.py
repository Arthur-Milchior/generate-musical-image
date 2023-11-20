from solfege.interval.too_big_alterations_exception import TooBigAlterationException
from solfege.interval.interval import Interval, TestInterval
from solfege.note import ChromaticNote, DiatonicNote, IntervalMode
from solfege.note.alteration import TEXT, LILY, Alteration


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

    def get_note_name(self, usage: str):
        """The name of this note.

        Args: usage -- see Alteration file."""
        diatonic = self.get_diatonic()
        alteration = self.get_alteration()
        return f"{diatonic.get_note_name(usage=usage)}{alteration.get_note_name(usage=usage)}"

    def correctAlteration(self):
        """Whether the note has a printable alteration."""
        return self.get_alteration().printable()

    def lily(self, use_color=True):
        """Lilypond representation of this note. Colored according to
        getColor, unless color is set to False.
        """
        diatonic = self.get_diatonic()
        try:
            alteration = self.get_alteration()
        except TooBigAlterationException as tba:
            tba["The note which is too big"] = self
            raise
        lily_code_for_black_note = f"{diatonic.get_note_name(usage=LILY)}{alteration.lily()}{self.get_diatonic().lily_octave()}"
        if not use_color:
            return lily_code_for_black_note
        return """\\tweak NoteHead.color  #(x11-color '{self.get_color()})\n{lily_code_for_black_note}\n"""

    def adjacent(self, other):
        """Whether `other` is at most two half-tone away"""
        return abs(other.get_number() - self.get_number()) <= 2

    def is_black_key_on_piano(self):
        """Whether this note corresponds to a black note of the keyboard"""
        blacks = {1, 3, 6, 8, 10}
        return (self.get_chromatic().get_number() % 12) in blacks

    @staticmethod
    def from_name(name: str):
        name = name.strip()
        diatonic_name = "".join(letter for letter in name if letter not in {"#", "♭"})
        alteration_name = "".join(letter for letter in name if letter in {"#", "♭"})
        diatonic = DiatonicNote.from_name(diatonic_name)
        chromatic_from_diatonic = diatonic.get_chromatic()
        alteration = Alteration.from_name(alteration_name)
        return Note(diatonic=diatonic.get_number(),
                    chromatic=(chromatic_from_diatonic + alteration).get_number())


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
        self.assertEquals(self.C4.lily(use_color=False), "c'")
        self.assertEquals(self.C3.lily(use_color=False), "c")
        self.assertEquals(self.C5.lily(use_color=False), "c''")
        self.assertEquals(self.B3.lily(use_color=False), "b")

    def test_is_black_key(self):
        self.assertFalse(self.C4.is_black_key_on_piano())
        self.assertTrue(self.C4_sharp.is_black_key_on_piano())

    def test_adjacent(self):
        self.assertTrue(self.C4.adjacent(self.C4))
        self.assertTrue(self.C4.adjacent(self.B3))
        self.assertTrue(self.C4.adjacent(self.C4_sharp))
        self.assertTrue(self.C4.adjacent(self.D4))
        self.assertFalse(self.C4.adjacent(self.D4_sharp))
        self.assertFalse(self.C4.adjacent(self.A3))
        self.assertTrue(self.C4.adjacent(self.B3_flat))

    def test_from_name(self):
        self.assertEquals(Note.from_name("C"), Note(chromatic=0, diatonic=0))
        self.assertEquals(Note.from_name("C4"), Note(chromatic=0, diatonic=0))
        self.assertEquals(Note.from_name("B3#"), Note(chromatic=0, diatonic=-1))
        self.assertEquals(Note.from_name("B#3"), Note(chromatic=0, diatonic=-1))

        self.assertEquals(Note.from_name("C♭"), Note(chromatic=-1, diatonic=0))
        self.assertEquals(Note.from_name("C4♭"), Note(chromatic=-1, diatonic=0))
        self.assertEquals(Note.from_name("C♭4"), Note(chromatic=-1, diatonic=0))
        self.assertEquals(Note.from_name("B3"), Note(chromatic=-1, diatonic=-1))

    # todo Test wwith color
