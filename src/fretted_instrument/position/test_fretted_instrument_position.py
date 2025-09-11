
import unittest

from fretted_instrument.fretted_instrument.fretted_instruments import Guitar
from solfege.value.note.note import Note
from fretted_instrument.position.fretted_instrument_position import *
from fretted_instrument.position.string.string_deltas import *

instrument = Guitar
strings = list(Guitar.strings())

def position_make(string, fret):
    return PositionOnFrettedInstrument(Guitar, string, fret)

empty_first_string = position_make(strings[0], instrument.fret(0))
E5 = ChromaticNote.from_name("E5")

E5_1 = position_make(strings[0], instrument.fret(24))
E5_2 = position_make(strings[1], instrument.fret(19))
E5_3 = position_make(strings[2], instrument.fret(14))
E5_4 = position_make(strings[3], instrument.fret(9))
E5_5 = position_make(strings[4], instrument.fret(5))
E5_6 = position_make(strings[5], instrument.fret(0))

not_played = Guitar.fret( value=None)

def frets_make(*args, **kwargs):
    return Frets.make(Guitar, *args, **kwargs)

class TestFrettedInstrumentPosition(unittest.TestCase):
    def test_get_chromatic(self):
        self.assertEqual(position_make(strings[0], fret=not_played).get_chromatic(), None)
        self.assertEqual(empty_first_string.get_chromatic(), ChromaticNote(value=-8))
        self.assertEqual(position_make(strings[2], instrument.fret(3)).get_chromatic(), ChromaticNote(value=5))

    # def test_svg(self):
    #     self.assertEqual(PositionOnFrettedInstrument(strings[0], fret=not_played).svg(), """<text x="15" y="16" font-size="30">x</text>""")
    #     self.assertEqual(empty_first_string.svg(), """<circle cx="15" cy="25" r="11" fill="white" stroke="black" stroke-width="3"/>""")
    #     self.assertEqual(PositionOnFrettedInstrument(strings[0], instrument.fret(3)).svg(), """<circle cx="15" cy="150" r="11" fill="black" stroke="black" stroke-width="3"/>""")

    def test_repr(self):
        self.assertEqual(repr(position_make(strings[0], fret=not_played)), "PositionOnFrettedInstrument.make(1, None)")
        self.assertEqual(repr(empty_first_string), "PositionOnFrettedInstrument.make(1, 0)")

    def test_eq(self):
        self.assertEqual(position_make(strings[0], fret=not_played), position_make(strings[0], fret=not_played))
        self.assertEqual(position_make(strings[0], instrument.fret(8)), position_make(strings[0], instrument.fret(8)))
        self.assertNotEqual(position_make(strings[1], instrument.fret(8)), position_make(strings[0], instrument.fret(8)))
        self.assertNotEqual(position_make(strings[0], instrument.fret(7)), position_make(strings[0], instrument.fret(8)))
        self.assertNotEqual(position_make(strings[0], fret=not_played), position_make(strings[0], instrument.fret(8)))

    def test_lt(self):
        self.assertLess( position_make(strings[0], instrument.fret(1)), position_make(strings[0], fret=not_played))
        self.assertLess(position_make(strings[0], instrument.fret(1)), position_make(strings[0], instrument.fret(2)))
        self.assertLess(position_make(strings[0], instrument.fret(1)), position_make(strings[1], instrument.fret(1)))
        self.assertLess(position_make(strings[0], instrument.fret(1)), position_make(strings[1], fret=not_played))

    def test_le(self):
        self.assertEqual(position_make(strings[0], fret=not_played), position_make(strings[0], fret=not_played))
        self.assertEqual(position_make(strings[0], instrument.fret(8)), position_make(strings[0], instrument.fret(8)))
        self.assertLessEqual(position_make(strings[0], instrument.fret(1)), position_make(strings[0], fret=not_played))
        self.assertLessEqual(position_make(strings[0], instrument.fret(1)), position_make(strings[0], instrument.fret(2)))
        self.assertLessEqual(position_make(strings[0], instrument.fret(1)), position_make(strings[1], instrument.fret(1)))
        self.assertLessEqual(position_make(strings[0], instrument.fret(1)), position_make(strings[1], fret=not_played))

    def test_from_chromatic(self):
        strings_interval = StringsInterval(Guitar, strings[3], strings[5])
        self.assertEqual(PositionOnFrettedInstrument.from_chromatic(Guitar, E5), 
                         [
                             E5_1,
                             E5_2,
                             E5_3,
                             E5_4,
                             E5_5,
                             E5_6,
                          ])
        self.assertEqual(PositionOnFrettedInstrument.from_chromatic(Guitar, E5, frets = frets_make((8, 15), True)), 
                         [
                             E5_3,
                             E5_4,
                             E5_6,
                          ])
        self.assertEqual(PositionOnFrettedInstrument.from_chromatic(Guitar, E5, frets = frets_make((8, 15), False)), 
                         [
                             E5_3,
                             E5_4,
                          ])
        self.assertEqual(PositionOnFrettedInstrument.from_chromatic(Guitar, E5, strings = strings_interval), 
                         [
                             E5_4,
                             E5_5,
                             E5_6,
                          ])
        self.assertEqual(PositionOnFrettedInstrument.from_chromatic(Guitar, E5, frets = frets_make((8, 15), True), strings = strings_interval), 
                         [
                             E5_4,
                             E5_6,
                          ])
        self.assertEqual(PositionOnFrettedInstrument.from_chromatic(Guitar, E5, frets = frets_make((8, 15), False), strings = strings_interval), 
                         [
                             E5_4,
                          ])
        
    def test_add(self):
        C5 = position_make(strings[0], instrument.fret(20))
        third_major = ChromaticInterval(4)
        self.assertEqual(C5.positions_for_interval_with_restrictions(third_major, strings=StringDelta.SAME_STRING_ONLY(Guitar)),
                         [E5_1,])
        self.assertEqual(C5.positions_for_interval_with_restrictions(third_major, strings=StringDelta.NEXT_STRING_ONLY(Guitar)),
                         [E5_2,])
        self.assertEqual(C5.positions_for_interval_with_restrictions(third_major, strings=StringDelta.SAME_OR_NEXT_STRING(Guitar)),
                         [E5_1, E5_2,])
        self.assertEqual(C5.positions_for_interval_with_restrictions(third_major, strings=StringDelta.SAME_STRING_OR_GREATER(Guitar)),
                         [E5_1, E5_2, E5_3, E5_4, E5_5, E5_6])
        self.assertEqual(C5.positions_for_interval_with_restrictions(third_major, strings=StringDelta.NEXT_STRING_OR_GREATER(Guitar)),
                         [E5_2, E5_3, E5_4, E5_5, E5_6])
        self.assertEqual(C5.positions_for_interval_with_restrictions(third_major, frets=frets_make((1, 5))),
                         [E5_5, E5_6])
        self.assertEqual(C5.positions_for_interval_with_restrictions(third_major, frets=frets_make((1, 5), False)),
                         [E5_5])
        
        # self.assertEqual(C5.positions_for_interval_with_restrictions(third_major, frets=frets_make().restrict_around(C5.fret)),
        #                  [E5_1, E5_2, E5_6])
        # self.assertEqual(C5.positions_for_interval_with_restrictions(third_major, frets=frets_make().restrict_around(C5.fret).disallow_open()),
        #                  [E5_1, E5_2])
        