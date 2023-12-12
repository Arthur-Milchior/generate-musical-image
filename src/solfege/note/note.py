from typing import Optional

from lily.Lilyable.local_lilyable import LocalLilyable
from solfege.interval.interval import Interval, TestInterval, third_minor
from solfege.note import ChromaticNote, DiatonicNote
from solfege.note.alteration import Alteration, alteration_symbols


class Note(Interval, ChromaticNote, LocalLilyable):
    IntervalClass = Interval
    DiatonicClass = DiatonicNote
    ChromaticClass = ChromaticNote
    """A note of the scale, as an interval from middle C."""

    def __init__(self, name: Optional[str] = None, *args, **kwargs):
        if name is not None:
            name = name.strip()
            diatonic_name = "".join(letter for letter in name if letter not in alteration_symbols)
            alteration_name = "".join(letter for letter in name if letter in alteration_symbols)
            diatonic = DiatonicNote.from_name(diatonic_name)
            chromatic_from_diatonic = diatonic.get_chromatic()
            alteration = Alteration.from_name(alteration_name)
            kwargs["diatonic"] = diatonic.get_number()
            kwargs["chromatic"] = (chromatic_from_diatonic + alteration).get_number()
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

    def lily_in_scale(self):
        return f"{self.get_diatonic().lily_in_scale()}{self.get_alteration().lily_in_scale()}{self.get_diatonic().get_octave_name_lily()}"

    def get_symbol_name(self):
        """The name of this note.

        Args: usage -- see Alteration file."""
        return f"{self.get_diatonic().get_name_up_to_octave()}{self.get_alteration().get_symbol_name()}"

    def get_ascii_name(self):
        """The name of this note.

        Args: usage -- see Alteration file."""
        return f"{self.get_diatonic().get_name_up_to_octave()}{self.get_alteration().get_ascii_name()}"

    def get_name_up_to_octave(self):
        raise NotImplemented

    def get_full_name(self):
        return f"{self.get_symbol_name()}{self.get_octave() + 4}"

    def correctAlteration(self):
        """Whether the note has a printable alteration."""
        return self.get_alteration().printable()

    def adjacent(self, other):
        """Whether `other` is at most two half-tone away"""
        return abs(other.get_number() - self.get_number()) <= 2

    def is_white_key_on_piano(self):
        """Whether this note corresponds to a black note of the keyboard"""
        return not self.is_black_key_on_piano()

    def is_black_key_on_piano(self):
        """Whether this note corresponds to a black note of the keyboard"""
        blacks = {1, 3, 6, 8, 10}
        return (self.get_chromatic().get_number() % 12) in blacks

    def simplest_enharmonic(self):
        """Enharmonic note, with 0 alteration if possible or one of the same alteration"""
        enharmonic = self
        while enharmonic.get_alteration().value >= 2:
            # double sharp at least, let's add a diatonic note
            enharmonic += Interval(diatonic=1, chromatic=0)
        while enharmonic.get_alteration().value <= -2:
            # double flat at least, let's remove a diatonic note
            enharmonic += Interval(diatonic=-1, chromatic=0)
        if enharmonic.get_alteration().value == 1:
            # It's a sharp note. Let's check if adding a diatonic note lead to a white key
            above = enharmonic + Interval(diatonic=1, chromatic=0)
            if above.is_white_key_on_piano():
                return above
        if enharmonic.get_alteration().value == -1:
            # It's a flat note. Let's check if removing a diatonic note lead to a white key
            below = enharmonic + Interval(diatonic=-1, chromatic=0)
            if below.is_white_key_on_piano():
                return below
        return enharmonic

    def canonize(self, for_sharp: bool):
        """Enharmonic note, with no alteration if possible or a single sharp"""
        enharmonic = self
        while enharmonic.get_alteration().value > (1 if for_sharp else 0):
            # too many sharp least, let's add a diatonic note
            enharmonic += Interval(diatonic=1, chromatic=0)
        while enharmonic.get_alteration().value < (0 if for_sharp else -1):
            # too many flat, let's remove a diatonic note
            enharmonic += Interval(diatonic=-1, chromatic=0)
        if enharmonic.get_alteration().value == 1:
            # It's a sharp note. Let's check if adding a diatonic note lead to a white key
            above = enharmonic + Interval(diatonic=1, chromatic=0)
            if above.is_white_key_on_piano():
                return above
        if enharmonic.get_alteration().value == -1:
            # It's a flat note. Let's check if removing a diatonic note lead to a white key
            below = enharmonic + Interval(diatonic=-1, chromatic=0)
            if below.is_white_key_on_piano():
                return below
        return enharmonic

    def is_natural(self):
        return self.get_alteration() == Alteration(0)

    def is_sharp(self):
        return self.get_alteration() == Alteration(1)

    def is_flat(self):
        return self.get_alteration() == Alteration(-1)

    def is_double_sharp(self):
        return self.get_alteration() == Alteration(2)

    def is_double_flat(self):
        return self.get_alteration() == Alteration(-2)

    @staticmethod
    def from_name(name: str):
        return Note(name)


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
        self.assertTrue(self.C4.adjacent(self.C4))
        self.assertTrue(self.C4.adjacent(self.B3))
        self.assertTrue(self.C4.adjacent(self.C4_sharp))
        self.assertTrue(self.C4.adjacent(self.D4))
        self.assertFalse(self.C4.adjacent(self.D4_sharp))
        self.assertFalse(self.C4.adjacent(self.A3))
        self.assertTrue(self.C4.adjacent(self.B3_flat))

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
