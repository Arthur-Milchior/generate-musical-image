import unittest

from solfege.list_order import ListOrder
from solfege.pattern_instantiation.scale.scale import Scale
from solfege.value.note.note import Note
from solfege.value.note.set.note_list import NoteList

from solfege.pattern.scale.scale_patterns import minor_melodic
C4 = Note.make(0, 0)
minor_melodic_C4 = Scale(minor_melodic, C4)

class TestScale(unittest.TestCase):
    def test_generate(self): 

        expected = NoteList.make(notes=[
            Note.make(0, 0),
            Note.make(2, 1),
            Note.make(3, 2),
            Note.make(5, 3),
            Note.make(7, 4),
            Note.make(9, 5),
            Note.make(11, 6),
            Note.make(12, 7),
        ], list_order=ListOrder.INCREASING)
        generated = minor_melodic_C4.get_notes()
        self.assertEqual(expected, generated)

    def test_generate_two(self): 
        expected = NoteList.make(notes=[
            Note.make(0, 0),
            Note.make(2, 1),
            Note.make(3, 2),
            Note.make(5, 3),
            Note.make(7, 4),
            Note.make(9, 5),
            Note.make(11, 6),
            Note.make(12, 7),
            Note.make(14, 8),
            Note.make(15, 9),
            Note.make(17, 10),
            Note.make(19, 11),
            Note.make(21, 12),
            Note.make(23, 13),
            Note.make(24, 14),
        ], list_order=ListOrder.INCREASING)
        generated = minor_melodic_C4.get_notes(number_of_octaves=2)
        self.assertEqual(expected, generated)

    def test_generate_two_extra(self):
        expected = NoteList.make(notes=[
            Note.make(0, 0),
            Note.make(2, 1),
            Note.make(3, 2),
            Note.make(5, 3),
            Note.make(7, 4),
            Note.make(9, 5),
            Note.make(11, 6),
            Note.make(12, 7),
            Note.make(14, 8),
            Note.make(15, 9),
            Note.make(17, 10),
            Note.make(19, 11),
            Note.make(21, 12),
            Note.make(23, 13),
            Note.make(24, 14),
            Note.make(26, 15),
        ], list_order=ListOrder.INCREASING)
        generated = minor_melodic_C4.get_notes(number_of_octaves=2, add_an_extra_note=True)
        self.assertEqual(expected, generated)

    def test_generate_minus_two(self):
        from solfege.pattern.scale.scale_patterns import minor_melodic
        expected = NoteList.make(notes=[
            Note.make(0, 0),
            Note.make(-1, -1),
            Note.make(-3, -2),
            Note.make(-5, -3),
            Note.make(-7, -4),
            Note.make(-9, -5),
            Note.make(-10, -6),
            Note.make(-12, -7),
            Note.make(-13, -8),
            Note.make(-15, -9),
            Note.make(-17, -10),
            Note.make(-19, -11),
            Note.make(-21, -12),
            Note.make(-22, -13),
            Note.make(-24, -14),
        ], list_order=ListOrder.DECREASING)
        generated = minor_melodic_C4.get_notes(number_of_octaves=-2)
        self.assertEqual(expected, generated)

    def test_generate_minus_two_extra(self):
        from solfege.pattern.scale.scale_patterns import minor_melodic
        expected = NoteList.make(notes=[
            Note.make(0, 0),
            Note.make(-1, -1),
            Note.make(-3, -2),
            Note.make(-5, -3),
            Note.make(-7, -4),
            Note.make(-9, -5),
            Note.make(-10, -6),
            Note.make(-12, -7),
            Note.make(-13, -8),
            Note.make(-15, -9),
            Note.make(-17, -10),
            Note.make(-19, -11),
            Note.make(-21, -12),
            Note.make(-22, -13),
            Note.make(-24, -14),
            Note.make(-25, -15),
        ], list_order=ListOrder.DECREASING)
        generated = minor_melodic_C4.get_notes(number_of_octaves=-2, add_an_extra_note=True)
        self.assertEqual(expected, generated)
