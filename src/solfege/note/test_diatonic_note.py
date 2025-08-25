from solfege.interval.test_diatonic_interval import TestDiatonicInterval
from solfege.note.abstract_note import OctaveOutput
from .diatonic_note import *


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
        from solfege.note.chromatic_note import ChromaticNote
        DiatonicNote.ChromaticClass = ChromaticNote

    def test_is_note(self):
        self.assertTrue(self.C4.is_note())

    def test_one_octave(self):
        self.assertEqual(DiatonicNote.get_one_octave(), DiatonicNote(7))


    def test_get_number(self):
        self.assertEqual(self.C4.value, 0)

    def test_equal(self):
        self.assertEqual(self.C4, self.C4)
        self.assertNotEqual(self.D4, self.C4)
        self.assertEqual(self.D4, self.D4)

    def test_add(self):
        self.assertEqual(self.D4 + self.third, self.F4)
        self.assertEqual(self.third + self.D4, self.F4)
        with self.assertRaises(Exception):
            _ = self.D4 + self.D4

    def test_neg(self):
        with self.assertRaises(Exception):
            _ = -self.D4

    def test_sub(self):
        self.assertEqual(self.F4 - self.third, self.D4)
        self.assertEqual(self.F4 - self.D4, self.third)
        with self.assertRaises(Exception):
            _ = self.third - self.D4

    def test_lt(self):
        self.assertLess(self.D4, self.F4)
        self.assertLessEqual(self.D4, self.F4)
        self.assertLessEqual(self.D4, self.D4)

    def test_repr(self):
        self.assertEqual(repr(self.D4), "DiatonicNote(value=1)")

    def test_octave(self):
        self.assertEqual(self.C4.octave(), 0)
        self.assertEqual(self.B4.octave(), 0)
        self.assertEqual(self.D3.octave(), -1)
        self.assertEqual(self.C3.octave(), -1)
        self.assertEqual(self.B2.octave(), -2)
        self.assertEqual(self.C5.octave(), 1)

    def test_add_octave(self):
        self.assertEqual(self.C5.add_octave(-1), self.C4)
        self.assertEqual(self.C4.add_octave(1), self.C5)
        self.assertEqual(self.C5.add_octave(-2), self.C3)
        self.assertEqual(self.C3.add_octave(2), self.C5)

    def test_same_note_in_base_octave(self):
        self.assertEqual(self.C5.in_base_octave(), self.C4)
        self.assertEqual(self.C3.in_base_octave(), self.C4)
        self.assertEqual(self.C4.in_base_octave(), self.C4)
        self.assertEqual(self.D4.in_base_octave(), self.D4)
        self.assertEqual(self.B3.in_base_octave(), self.B4)

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
        from solfege.note.chromatic_note import ChromaticNote
        self.assertEqual(DiatonicNote(0).get_chromatic(), ChromaticNote(0))
        self.assertEqual(DiatonicNote(1).get_chromatic(), ChromaticNote(2))
        self.assertEqual(DiatonicNote(2).get_chromatic(), ChromaticNote(4))
        self.assertEqual(DiatonicNote(3).get_chromatic(), ChromaticNote(5))
        self.assertEqual(DiatonicNote(4).get_chromatic(), ChromaticNote(7))
        self.assertEqual(DiatonicNote(5).get_chromatic(), ChromaticNote(9))
        self.assertEqual(DiatonicNote(6).get_chromatic(), ChromaticNote(11))
        self.assertEqual(DiatonicNote(7).get_chromatic(), ChromaticNote(12))
        self.assertEqual(DiatonicNote(8).get_chromatic(), ChromaticNote(14))
        self.assertEqual(DiatonicNote(9).get_chromatic(), ChromaticNote(16))
        self.assertEqual(DiatonicNote(-1).get_chromatic(), ChromaticNote(-1))
        self.assertEqual(DiatonicNote(-2).get_chromatic(), ChromaticNote(-3))
        self.assertEqual(DiatonicNote(-3).get_chromatic(), ChromaticNote(-5))
        self.assertEqual(DiatonicNote(-4).get_chromatic(), ChromaticNote(-7))
        self.assertEqual(DiatonicNote(-5).get_chromatic(), ChromaticNote(-8))
        self.assertEqual(DiatonicNote(-6).get_chromatic(), ChromaticNote(-10))
        self.assertEqual(DiatonicNote(-7).get_chromatic(), ChromaticNote(-12))
        self.assertEqual(DiatonicNote(-8).get_chromatic(), ChromaticNote(-13))
        self.assertEqual(DiatonicNote(-9).get_chromatic(), ChromaticNote(-15))

    def test_get_note_name_LILY(self):
        self.assertEqual(DiatonicNote(0).get_name_up_to_octave(note_output = NoteOutput.LILY, fixed_length=FixedLengthOutput.NO, ), "c")
        self.assertEqual(DiatonicNote(1).get_name_up_to_octave(note_output = NoteOutput.LILY, fixed_length=FixedLengthOutput.NO, ), "d")
        self.assertEqual(DiatonicNote(2).get_name_up_to_octave(note_output = NoteOutput.LILY, fixed_length=FixedLengthOutput.NO, ), "e")
        self.assertEqual(DiatonicNote(3).get_name_up_to_octave(note_output = NoteOutput.LILY, fixed_length=FixedLengthOutput.NO, ), "f")
        self.assertEqual(DiatonicNote(4).get_name_up_to_octave(note_output = NoteOutput.LILY, fixed_length=FixedLengthOutput.NO, ), "g")
        self.assertEqual(DiatonicNote(5).get_name_up_to_octave(note_output = NoteOutput.LILY, fixed_length=FixedLengthOutput.NO, ), "a")
        self.assertEqual(DiatonicNote(6).get_name_up_to_octave(note_output = NoteOutput.LILY, fixed_length=FixedLengthOutput.NO, ), "b")
        self.assertEqual(DiatonicNote(7).get_name_up_to_octave(note_output = NoteOutput.LILY, fixed_length=FixedLengthOutput.NO, ), "c")
        self.assertEqual(DiatonicNote(8).get_name_up_to_octave(note_output = NoteOutput.LILY, fixed_length=FixedLengthOutput.NO, ), "d")
        self.assertEqual(DiatonicNote(9).get_name_up_to_octave(note_output = NoteOutput.LILY, fixed_length=FixedLengthOutput.NO, ), "e")
        self.assertEqual(DiatonicNote(-1).get_name_up_to_octave(note_output = NoteOutput.LILY, fixed_length=FixedLengthOutput.NO, ), "b")
        self.assertEqual(DiatonicNote(-2).get_name_up_to_octave(note_output = NoteOutput.LILY, fixed_length=FixedLengthOutput.NO, ), "a")
        self.assertEqual(DiatonicNote(-3).get_name_up_to_octave(note_output = NoteOutput.LILY, fixed_length=FixedLengthOutput.NO, ), "g")
        self.assertEqual(DiatonicNote(-4).get_name_up_to_octave(note_output = NoteOutput.LILY, fixed_length=FixedLengthOutput.NO, ), "f")
        self.assertEqual(DiatonicNote(-5).get_name_up_to_octave(note_output = NoteOutput.LILY, fixed_length=FixedLengthOutput.NO, ), "e")
        self.assertEqual(DiatonicNote(-6).get_name_up_to_octave(note_output = NoteOutput.LILY, fixed_length=FixedLengthOutput.NO, ), "d")
        self.assertEqual(DiatonicNote(-7).get_name_up_to_octave(note_output = NoteOutput.LILY, fixed_length=FixedLengthOutput.NO, ), "c")
        self.assertEqual(DiatonicNote(-8).get_name_up_to_octave(note_output = NoteOutput.LILY, fixed_length=FixedLengthOutput.NO, ), "b")
        self.assertEqual(DiatonicNote(-9).get_name_up_to_octave(note_output = NoteOutput.LILY, fixed_length=FixedLengthOutput.NO, ), "a")

    def test_get_note_name_FILE_NAME(self):
        self.assertEqual(DiatonicNote(0).get_name_up_to_octave(note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "C")
        self.assertEqual(DiatonicNote(1).get_name_up_to_octave(note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "D")
        self.assertEqual(DiatonicNote(2).get_name_up_to_octave(note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "E")
        self.assertEqual(DiatonicNote(3).get_name_up_to_octave(note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "F")
        self.assertEqual(DiatonicNote(4).get_name_up_to_octave(note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "G")
        self.assertEqual(DiatonicNote(5).get_name_up_to_octave(note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "A")
        self.assertEqual(DiatonicNote(6).get_name_up_to_octave(note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "B")
        self.assertEqual(DiatonicNote(7).get_name_up_to_octave(note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "C")
        self.assertEqual(DiatonicNote(8).get_name_up_to_octave(note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "D")
        self.assertEqual(DiatonicNote(9).get_name_up_to_octave(note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "E")
        self.assertEqual(DiatonicNote(-1).get_name_up_to_octave(note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "B")
        self.assertEqual(DiatonicNote(-2).get_name_up_to_octave(note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "A")
        self.assertEqual(DiatonicNote(-3).get_name_up_to_octave(note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "G")
        self.assertEqual(DiatonicNote(-4).get_name_up_to_octave(note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "F")
        self.assertEqual(DiatonicNote(-5).get_name_up_to_octave(note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "E")
        self.assertEqual(DiatonicNote(-6).get_name_up_to_octave(note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "D")
        self.assertEqual(DiatonicNote(-7).get_name_up_to_octave(note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "C")
        self.assertEqual(DiatonicNote(-8).get_name_up_to_octave(note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "B")
        self.assertEqual(DiatonicNote(-9).get_name_up_to_octave(note_output=NoteOutput.LETTER, fixed_length=FixedLengthOutput.NO), "A")

    def test_get_octave_name_LILY(self):
        self.assertEqual(DiatonicNote(0).get_octave_name(octave_notation=OctaveOutput.LILY), "'")
        self.assertEqual(DiatonicNote(1).get_octave_name(octave_notation=OctaveOutput.LILY), "'")
        self.assertEqual(DiatonicNote(2).get_octave_name(octave_notation=OctaveOutput.LILY), "'")
        self.assertEqual(DiatonicNote(3).get_octave_name(octave_notation=OctaveOutput.LILY), "'")
        self.assertEqual(DiatonicNote(4).get_octave_name(octave_notation=OctaveOutput.LILY), "'")
        self.assertEqual(DiatonicNote(5).get_octave_name(octave_notation=OctaveOutput.LILY), "'")
        self.assertEqual(DiatonicNote(6).get_octave_name(octave_notation=OctaveOutput.LILY), "'")
        self.assertEqual(DiatonicNote(7).get_octave_name(octave_notation=OctaveOutput.LILY), "''")
        self.assertEqual(DiatonicNote(8).get_octave_name(octave_notation=OctaveOutput.LILY), "''")
        self.assertEqual(DiatonicNote(9).get_octave_name(octave_notation=OctaveOutput.LILY), "''")
        self.assertEqual(DiatonicNote(-1).get_octave_name(octave_notation=OctaveOutput.LILY), "")
        self.assertEqual(DiatonicNote(-2).get_octave_name(octave_notation=OctaveOutput.LILY), "")
        self.assertEqual(DiatonicNote(-3).get_octave_name(octave_notation=OctaveOutput.LILY), "")
        self.assertEqual(DiatonicNote(-4).get_octave_name(octave_notation=OctaveOutput.LILY), "")
        self.assertEqual(DiatonicNote(-5).get_octave_name(octave_notation=OctaveOutput.LILY), "")
        self.assertEqual(DiatonicNote(-6).get_octave_name(octave_notation=OctaveOutput.LILY), "")
        self.assertEqual(DiatonicNote(-7).get_octave_name(octave_notation=OctaveOutput.LILY), "")
        self.assertEqual(DiatonicNote(-8).get_octave_name(octave_notation=OctaveOutput.LILY), ",")
        self.assertEqual(DiatonicNote(-9).get_octave_name(octave_notation=OctaveOutput.LILY), ",")

    def test_get_octave_name_FILE_NAME(self):
        self.assertEqual(DiatonicNote(0).get_octave_name(octave_notation = OctaveOutput.MIDDLE_IS_4), "4")
        self.assertEqual(DiatonicNote(1).get_octave_name(octave_notation = OctaveOutput.MIDDLE_IS_4), "4")
        self.assertEqual(DiatonicNote(2).get_octave_name(octave_notation = OctaveOutput.MIDDLE_IS_4), "4")
        self.assertEqual(DiatonicNote(3).get_octave_name(octave_notation = OctaveOutput.MIDDLE_IS_4), "4")
        self.assertEqual(DiatonicNote(4).get_octave_name(octave_notation = OctaveOutput.MIDDLE_IS_4), "4")
        self.assertEqual(DiatonicNote(5).get_octave_name(octave_notation = OctaveOutput.MIDDLE_IS_4), "4")
        self.assertEqual(DiatonicNote(6).get_octave_name(octave_notation = OctaveOutput.MIDDLE_IS_4), "4")
        self.assertEqual(DiatonicNote(7).get_octave_name(octave_notation = OctaveOutput.MIDDLE_IS_4), "5")
        self.assertEqual(DiatonicNote(8).get_octave_name(octave_notation = OctaveOutput.MIDDLE_IS_4), "5")
        self.assertEqual(DiatonicNote(9).get_octave_name(octave_notation = OctaveOutput.MIDDLE_IS_4), "5")
        self.assertEqual(DiatonicNote(-1).get_octave_name(octave_notation = OctaveOutput.MIDDLE_IS_4), "3")
        self.assertEqual(DiatonicNote(-2).get_octave_name(octave_notation = OctaveOutput.MIDDLE_IS_4), "3")
        self.assertEqual(DiatonicNote(-3).get_octave_name(octave_notation = OctaveOutput.MIDDLE_IS_4), "3")
        self.assertEqual(DiatonicNote(-4).get_octave_name(octave_notation = OctaveOutput.MIDDLE_IS_4), "3")
        self.assertEqual(DiatonicNote(-5).get_octave_name(octave_notation = OctaveOutput.MIDDLE_IS_4), "3")
        self.assertEqual(DiatonicNote(-6).get_octave_name(octave_notation = OctaveOutput.MIDDLE_IS_4), "3")
        self.assertEqual(DiatonicNote(-7).get_octave_name(octave_notation = OctaveOutput.MIDDLE_IS_4), "3")
        self.assertEqual(DiatonicNote(-8).get_octave_name(octave_notation = OctaveOutput.MIDDLE_IS_4), "2")
        self.assertEqual(DiatonicNote(-9).get_octave_name(octave_notation = OctaveOutput.MIDDLE_IS_4), "2")

    def test_from_name(self):
        self.assertEqual(DiatonicNote(0), DiatonicNote.from_name("C"))
        self.assertEqual(DiatonicNote(0), DiatonicNote.from_name("c"))
        self.assertEqual(DiatonicNote(0), DiatonicNote.from_name("c4"))
        self.assertEqual(DiatonicNote(-7), DiatonicNote.from_name("c3"))
        self.assertEqual(DiatonicNote(7), DiatonicNote.from_name("c5"))
        self.assertEqual(DiatonicNote(6), DiatonicNote.from_name("b4"))
        self.assertEqual(DiatonicNote(-1), DiatonicNote.from_name("b3"))
        self.assertEqual(DiatonicNote(13), DiatonicNote.from_name("b5"))
