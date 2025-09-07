
import unittest

from guitar.position.fret.fret import NOT_PLAYED
from solfege.value.note.note import Note
from guitar.position.guitar_position import *
from guitar.position.string.string import strings
from guitar.position.string.string_deltas import *
from guitar.position.string.strings import StringsInterval

empty_first_string = GuitarPosition(strings[0], Fret(0))
E5 = ChromaticNote.from_name("E5")

E5_1 = GuitarPosition(strings[0], Fret(24))
E5_2 = GuitarPosition(strings[1], Fret(19))
E5_3 = GuitarPosition(strings[2], Fret(14))
E5_4 = GuitarPosition(strings[3], Fret(9))
E5_5 = GuitarPosition(strings[4], Fret(5))
E5_6 = GuitarPosition(strings[5], Fret(0))
class TestGuitarPosition(unittest.TestCase):
    def test_get_chromatic(self):
        self.assertEqual(GuitarPosition(strings[0], fret=NOT_PLAYED).get_chromatic(), None)
        self.assertEqual(empty_first_string.get_chromatic(), ChromaticNote(value=-8))
        self.assertEqual(GuitarPosition(strings[2], Fret(3)).get_chromatic(), ChromaticNote(value=5))

    # def test_svg(self):
    #     self.assertEqual(GuitarPosition(strings[0], fret=NOT_PLAYED).svg(), """<text x="15" y="16" font-size="30">x</text>""")
    #     self.assertEqual(empty_first_string.svg(), """<circle cx="15" cy="25" r="11" fill="white" stroke="black" stroke-width="3"/>""")
    #     self.assertEqual(GuitarPosition(strings[0], Fret(3)).svg(), """<circle cx="15" cy="150" r="11" fill="black" stroke="black" stroke-width="3"/>""")

    def test_repr(self):
        self.assertEqual(repr(GuitarPosition(strings[0], fret=NOT_PLAYED)), "GuitarPosition.make(1, None)")
        self.assertEqual(repr(empty_first_string), "GuitarPosition.make(1, 0)")

    def test_eq(self):
        self.assertEqual(GuitarPosition(strings[0], fret=NOT_PLAYED), GuitarPosition(strings[0], fret=NOT_PLAYED))
        self.assertEqual(GuitarPosition(strings[0], Fret(8)), GuitarPosition(strings[0], Fret(8)))
        self.assertNotEqual(GuitarPosition(strings[1], Fret(8)), GuitarPosition(strings[0], Fret(8)))
        self.assertNotEqual(GuitarPosition(strings[0], Fret(7)), GuitarPosition(strings[0], Fret(8)))
        self.assertNotEqual(GuitarPosition(strings[0], fret=NOT_PLAYED), GuitarPosition(strings[0], Fret(8)))

    def test_lt(self):
        self.assertLess( GuitarPosition(strings[0], Fret(1)), GuitarPosition(strings[0], fret=NOT_PLAYED))
        self.assertLess(GuitarPosition(strings[0], Fret(1)), GuitarPosition(strings[0], Fret(2)))
        self.assertLess(GuitarPosition(strings[0], Fret(1)), GuitarPosition(strings[1], Fret(1)))
        self.assertLess(GuitarPosition(strings[0], Fret(1)), GuitarPosition(strings[1], fret=NOT_PLAYED))

    def test_le(self):
        self.assertEqual(GuitarPosition(strings[0], fret=NOT_PLAYED), GuitarPosition(strings[0], fret=NOT_PLAYED))
        self.assertEqual(GuitarPosition(strings[0], Fret(8)), GuitarPosition(strings[0], Fret(8)))
        self.assertLessEqual(GuitarPosition(strings[0], Fret(1)), GuitarPosition(strings[0], fret=NOT_PLAYED))
        self.assertLessEqual(GuitarPosition(strings[0], Fret(1)), GuitarPosition(strings[0], Fret(2)))
        self.assertLessEqual(GuitarPosition(strings[0], Fret(1)), GuitarPosition(strings[1], Fret(1)))
        self.assertLessEqual(GuitarPosition(strings[0], Fret(1)), GuitarPosition(strings[1], fret=NOT_PLAYED))

    def test_from_chromatic(self):
        strings_interval = StringsInterval(strings[3], strings[5])
        self.assertEqual(GuitarPosition.from_chromatic(E5), 
                         [
                             E5_1,
                             E5_2,
                             E5_3,
                             E5_4,
                             E5_5,
                             E5_6,
                          ])
        self.assertEqual(GuitarPosition.from_chromatic(E5, frets = Frets.make((8, 15), True)), 
                         [
                             E5_3,
                             E5_4,
                             E5_6,
                          ])
        self.assertEqual(GuitarPosition.from_chromatic(E5, frets = Frets.make((8, 15), False)), 
                         [
                             E5_3,
                             E5_4,
                          ])
        self.assertEqual(GuitarPosition.from_chromatic(E5, strings = strings_interval), 
                         [
                             E5_4,
                             E5_5,
                             E5_6,
                          ])
        self.assertEqual(GuitarPosition.from_chromatic(E5, frets = Frets.make((8, 15), True), strings = strings_interval), 
                         [
                             E5_4,
                             E5_6,
                          ])
        self.assertEqual(GuitarPosition.from_chromatic(E5, frets = Frets.make((8, 15), False), strings = strings_interval), 
                         [
                             E5_4,
                          ])
        
    def test_add(self):
        C5 = GuitarPosition(strings[0], Fret(20))
        third_major = ChromaticInterval(4)
        self.assertEqual(C5.positions_for_interval_with_restrictions(third_major, strings=SAME_STRING_ONLY),
                         [E5_1,])
        self.assertEqual(C5.positions_for_interval_with_restrictions(third_major, strings=NEXT_STRING_ONLY),
                         [E5_2,])
        self.assertEqual(C5.positions_for_interval_with_restrictions(third_major, strings=SAME_OR_NEXT_STRING),
                         [E5_1, E5_2,])
        self.assertEqual(C5.positions_for_interval_with_restrictions(third_major, strings=SAME_STRING_OR_GREATER),
                         [E5_1, E5_2, E5_3, E5_4, E5_5, E5_6])
        self.assertEqual(C5.positions_for_interval_with_restrictions(third_major, strings=NEXT_STRING_OR_GREATER),
                         [E5_2, E5_3, E5_4, E5_5, E5_6])
        self.assertEqual(C5.positions_for_interval_with_restrictions(third_major, frets=Frets.make((1, 5))),
                         [E5_5, E5_6])
        self.assertEqual(C5.positions_for_interval_with_restrictions(third_major, frets=Frets.make((1, 5), False)),
                         [E5_5])
        self.assertEqual(C5.positions_for_interval_with_restrictions(third_major, frets=Frets.make().restrict_around(C5.fret)),
                         [E5_1, E5_2, E5_6])
        self.assertEqual(C5.positions_for_interval_with_restrictions(third_major, frets=Frets.make().restrict_around(C5.fret).disallow_open()),
                         [E5_1, E5_2])
        