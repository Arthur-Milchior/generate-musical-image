from __future__ import annotations

from solfege.interval.diatonic import DiatonicInterval, TestDiatonicInterval
from solfege.note.abstract import AbstractNote
from solfege.note.alteration import LILY, FILE_NAME, FULL_NAME, DEBUG, NAME_UP_TO_OCTAVE


class DiatonicNote(AbstractNote, DiatonicInterval):
    """A diatonic note"""
    # Saved as the interval from middle C
    IntervalClass = DiatonicInterval

    def lily_in_scale(self):
        return ["c", "d", "e", "f", "g", "a", "b"][self.get_number() % 7]

    def get_name_up_to_octave(self):
        return ["C", "D", "E", "F", "G", "A", "B"][self.get_number() % 7]

    def get_octave_name_lily(self):
        """How to write the octave.

        Example: "'"
        """
        # must be separated from note name, because, in lilypond, the alteration is between the note name and the octave
        if self.get_octave() >= 0:
            return "'" * (self.get_octave()+1)
        return "," * (-self.get_octave()-1)

    def get_octave_name_ascii(self):
        """How to write the octave.

        Example: 4
        """
        # must be separated from note name, because, in lilypond, the alteration is between the note name and the octave
        return str(self.get_octave(scientificNotation=True))

    @staticmethod
    def from_name(name: str):
        assert 1 <= len(name) <= 2
        letter = name[0].lower()
        note = DiatonicNote({"c": 0, "d": 1, "e": 2, "f": 3, "g": 4, "a": 5, "b": 6}[letter])
        if len(name) == 2:
            octave = int(name[1])
            note = note.add_octave(octave - 4)
        return note


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

    def setUp(self):
        super().setUp()
        from solfege.note.chromatic import ChromaticNote
        DiatonicNote.RelatedChromaticClass = ChromaticNote

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

    def test_get_note_name_LILY(self):
        self.assertEquals(DiatonicNote(0).lily_in_scale(), "c")
        self.assertEquals(DiatonicNote(1).lily_in_scale(), "d")
        self.assertEquals(DiatonicNote(2).lily_in_scale(), "e")
        self.assertEquals(DiatonicNote(3).lily_in_scale(), "f")
        self.assertEquals(DiatonicNote(4).lily_in_scale(), "g")
        self.assertEquals(DiatonicNote(5).lily_in_scale(), "a")
        self.assertEquals(DiatonicNote(6).lily_in_scale(), "b")
        self.assertEquals(DiatonicNote(7).lily_in_scale(), "c")
        self.assertEquals(DiatonicNote(8).lily_in_scale(), "d")
        self.assertEquals(DiatonicNote(9).lily_in_scale(), "e")
        self.assertEquals(DiatonicNote(-1).lily_in_scale(), "b")
        self.assertEquals(DiatonicNote(-2).lily_in_scale(), "a")
        self.assertEquals(DiatonicNote(-3).lily_in_scale(), "g")
        self.assertEquals(DiatonicNote(-4).lily_in_scale(), "f")
        self.assertEquals(DiatonicNote(-5).lily_in_scale(), "e")
        self.assertEquals(DiatonicNote(-6).lily_in_scale(), "d")
        self.assertEquals(DiatonicNote(-7).lily_in_scale(), "c")
        self.assertEquals(DiatonicNote(-8).lily_in_scale(), "b")
        self.assertEquals(DiatonicNote(-9).lily_in_scale(), "a")

    def test_get_note_name_FILE_NAME(self):
        self.assertEquals(DiatonicNote(0).get_name_up_to_octave(), "C")
        self.assertEquals(DiatonicNote(1).get_name_up_to_octave(), "D")
        self.assertEquals(DiatonicNote(2).get_name_up_to_octave(), "E")
        self.assertEquals(DiatonicNote(3).get_name_up_to_octave(), "F")
        self.assertEquals(DiatonicNote(4).get_name_up_to_octave(), "G")
        self.assertEquals(DiatonicNote(5).get_name_up_to_octave(), "A")
        self.assertEquals(DiatonicNote(6).get_name_up_to_octave(), "B")
        self.assertEquals(DiatonicNote(7).get_name_up_to_octave(), "C")
        self.assertEquals(DiatonicNote(8).get_name_up_to_octave(), "D")
        self.assertEquals(DiatonicNote(9).get_name_up_to_octave(), "E")
        self.assertEquals(DiatonicNote(-1).get_name_up_to_octave(), "B")
        self.assertEquals(DiatonicNote(-2).get_name_up_to_octave(), "A")
        self.assertEquals(DiatonicNote(-3).get_name_up_to_octave(), "G")
        self.assertEquals(DiatonicNote(-4).get_name_up_to_octave(), "F")
        self.assertEquals(DiatonicNote(-5).get_name_up_to_octave(), "E")
        self.assertEquals(DiatonicNote(-6).get_name_up_to_octave(), "D")
        self.assertEquals(DiatonicNote(-7).get_name_up_to_octave(), "C")
        self.assertEquals(DiatonicNote(-8).get_name_up_to_octave(), "B")
        self.assertEquals(DiatonicNote(-9).get_name_up_to_octave(), "A")

    def test_get_octave_name_LILY(self):
        self.assertEquals(DiatonicNote(0).get_octave_name_lily(), "'")
        self.assertEquals(DiatonicNote(1).get_octave_name_lily(), "'")
        self.assertEquals(DiatonicNote(2).get_octave_name_lily(), "'")
        self.assertEquals(DiatonicNote(3).get_octave_name_lily(), "'")
        self.assertEquals(DiatonicNote(4).get_octave_name_lily(), "'")
        self.assertEquals(DiatonicNote(5).get_octave_name_lily(), "'")
        self.assertEquals(DiatonicNote(6).get_octave_name_lily(), "'")
        self.assertEquals(DiatonicNote(7).get_octave_name_lily(), "''")
        self.assertEquals(DiatonicNote(8).get_octave_name_lily(), "''")
        self.assertEquals(DiatonicNote(9).get_octave_name_lily(), "''")
        self.assertEquals(DiatonicNote(-1).get_octave_name_lily(), "")
        self.assertEquals(DiatonicNote(-2).get_octave_name_lily(), "")
        self.assertEquals(DiatonicNote(-3).get_octave_name_lily(), "")
        self.assertEquals(DiatonicNote(-4).get_octave_name_lily(), "")
        self.assertEquals(DiatonicNote(-5).get_octave_name_lily(), "")
        self.assertEquals(DiatonicNote(-6).get_octave_name_lily(), "")
        self.assertEquals(DiatonicNote(-7).get_octave_name_lily(), "")
        self.assertEquals(DiatonicNote(-8).get_octave_name_lily(), ",")
        self.assertEquals(DiatonicNote(-9).get_octave_name_lily(), ",")

    def test_get_octave_name_FILE_NAME(self):
        self.assertEquals(DiatonicNote(0).get_octave_name_ascii(), "4")
        self.assertEquals(DiatonicNote(1).get_octave_name_ascii(), "4")
        self.assertEquals(DiatonicNote(2).get_octave_name_ascii(), "4")
        self.assertEquals(DiatonicNote(3).get_octave_name_ascii(), "4")
        self.assertEquals(DiatonicNote(4).get_octave_name_ascii(), "4")
        self.assertEquals(DiatonicNote(5).get_octave_name_ascii(), "4")
        self.assertEquals(DiatonicNote(6).get_octave_name_ascii(), "4")
        self.assertEquals(DiatonicNote(7).get_octave_name_ascii(), "5")
        self.assertEquals(DiatonicNote(8).get_octave_name_ascii(), "5")
        self.assertEquals(DiatonicNote(9).get_octave_name_ascii(), "5")
        self.assertEquals(DiatonicNote(-1).get_octave_name_ascii(), "3")
        self.assertEquals(DiatonicNote(-2).get_octave_name_ascii(), "3")
        self.assertEquals(DiatonicNote(-3).get_octave_name_ascii(), "3")
        self.assertEquals(DiatonicNote(-4).get_octave_name_ascii(), "3")
        self.assertEquals(DiatonicNote(-5).get_octave_name_ascii(), "3")
        self.assertEquals(DiatonicNote(-6).get_octave_name_ascii(), "3")
        self.assertEquals(DiatonicNote(-7).get_octave_name_ascii(), "3")
        self.assertEquals(DiatonicNote(-8).get_octave_name_ascii(), "2")
        self.assertEquals(DiatonicNote(-9).get_octave_name_ascii(), "2")

    def test_from_name(self):
        self.assertEquals(DiatonicNote(0), DiatonicNote.from_name("C"))
        self.assertEquals(DiatonicNote(0), DiatonicNote.from_name("c"))
        self.assertEquals(DiatonicNote(0), DiatonicNote.from_name("c4"))
        self.assertEquals(DiatonicNote(-7), DiatonicNote.from_name("c3"))
        self.assertEquals(DiatonicNote(7), DiatonicNote.from_name("c5"))
        self.assertEquals(DiatonicNote(6), DiatonicNote.from_name("b4"))
        self.assertEquals(DiatonicNote(-1), DiatonicNote.from_name("b3"))
        self.assertEquals(DiatonicNote(13), DiatonicNote.from_name("b5"))
