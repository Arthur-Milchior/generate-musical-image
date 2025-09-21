
import unittest

from instruments.fretted_instrument.fretted_instrument.fretted_instruments import Guitar
from solfege.value.note.note import Note
from instruments.fretted_instrument.position.fretted_instrument_position import *
from instruments.fretted_instrument.position.string.string_deltas import *

instrument = Guitar
strings = list(Guitar.strings())

def position_make(string, fret):
    return PositionOnFrettedInstrument(string, fret)

empty_first_string = position_make(strings[0], Fret.make(0, True))
E5 = ChromaticNote.from_name("E5")

E5_1 = position_make(strings[0], Fret.make(24, True))
E5_2 = position_make(strings[1], Fret.make(19, True))
E5_3 = position_make(strings[2], Fret.make(14, True))
E5_4 = position_make(strings[3], Fret.make(9, True))
E5_5 = position_make(strings[4], Fret.make(5, True))
E5_6 = position_make(strings[5], Fret.make(0, True))

not_played = Fret.make( None, True)

def frets_make(*args, **kwargs):
    if "absolute" not in kwargs:
        args = [True] + list(args) 
    return Frets.make(*args, **kwargs)

class TestFrettedInstrumentPosition(unittest.TestCase):
    def test_get_chromatic(self):
        self.assertEqual(position_make(strings[0], fret=not_played).get_chromatic(), None)
        self.assertEqual(empty_first_string.get_chromatic(), ChromaticNote(value=-8))
        self.assertEqual(position_make(strings[2], Fret.make(3, True)).get_chromatic(), ChromaticNote(value=5))

    # def test_svg(self):
    #     self.assertEqual(PositionOnFrettedInstrument(strings[0], fret=not_played).svg(), """<text x="15" y="16" font-size="30">x</text>""")
    #     self.assertEqual(empty_first_string.svg(), """<circle cx="15" cy="25" r="11" fill="white" stroke="black" stroke-width="3"/>""")
    #     self.assertEqual(PositionOnFrettedInstrument(strings[0], Fret.make(3, True)).svg(), """<circle cx="15" cy="150" r="11" fill="black" stroke="black" stroke-width="3"/>""")

    def test_repr(self):
        self.assertEqual(repr(position_make(strings[0], fret=not_played)), "PositionOnFrettedInstrument.make(1, None)")
        self.assertEqual(repr(empty_first_string), "PositionOnFrettedInstrument.make(1, 0)")

    def test_eq(self):
        self.assertEqual(position_make(strings[0], fret=not_played), position_make(strings[0], fret=not_played))
        self.assertEqual(position_make(strings[0], Fret.make(8, True)), position_make(strings[0], Fret.make(8, True)))
        self.assertNotEqual(position_make(strings[1], Fret.make(8, True)), position_make(strings[0], Fret.make(8, True)))
        self.assertNotEqual(position_make(strings[0], Fret.make(7, True)), position_make(strings[0], Fret.make(8, True)))
        self.assertNotEqual(position_make(strings[0], fret=not_played), position_make(strings[0], Fret.make(8, True)))

    def test_lt(self):
        self.assertLess( position_make(strings[0], Fret.make(1, True)), position_make(strings[0], fret=not_played))
        self.assertLess(position_make(strings[0], Fret.make(1, True)), position_make(strings[0], Fret.make(2, True)))
        self.assertLess(position_make(strings[0], Fret.make(1, True)), position_make(strings[1], Fret.make(1, True)))
        self.assertLess(position_make(strings[0], Fret.make(1, True)), position_make(strings[1], fret=not_played))

    def test_le(self):
        self.assertEqual(position_make(strings[0], fret=not_played), position_make(strings[0], fret=not_played))
        self.assertEqual(position_make(strings[0], Fret.make(8, True)), position_make(strings[0], Fret.make(8, True)))
        self.assertLessEqual(position_make(strings[0], Fret.make(1, True)), position_make(strings[0], fret=not_played))
        self.assertLessEqual(position_make(strings[0], Fret.make(1, True)), position_make(strings[0], Fret.make(2, True)))
        self.assertLessEqual(position_make(strings[0], Fret.make(1, True)), position_make(strings[1], Fret.make(1, True)))
        self.assertLessEqual(position_make(strings[0], Fret.make(1, True)), position_make(strings[1], fret=not_played))

    def test_from_chromatic(self):
        strings_interval = Strings.make_interval(Guitar, strings[3], strings[5])
        self.assertEqual(PositionOnFrettedInstrument.from_chromatic(Guitar, E5, True),
                         [
                             E5_1,
                             E5_2,
                             E5_3,
                             E5_4,
                             E5_5,
                             E5_6,
                          ])
        self.assertEqual(PositionOnFrettedInstrument.from_chromatic(Guitar, E5, True,  frets = frets_make((8, 15), True)), 
                         [
                             E5_3,
                             E5_4,
                             E5_6,
                          ])
        self.assertEqual(PositionOnFrettedInstrument.from_chromatic(Guitar, E5, True,  frets = frets_make((8, 15), False)), 
                         [
                             E5_3,
                             E5_4,
                          ])
        self.assertEqual(PositionOnFrettedInstrument.from_chromatic(Guitar, E5, True,  strings = strings_interval), 
                         [
                             E5_4,
                             E5_5,
                             E5_6,
                          ])
        self.assertEqual(PositionOnFrettedInstrument.from_chromatic(Guitar, E5, True,  frets = frets_make((8, 15), True), strings = strings_interval), 
                         [
                             E5_4,
                             E5_6,
                          ])
        self.assertEqual(PositionOnFrettedInstrument.from_chromatic(Guitar, E5, True,  frets = frets_make((8, 15), False), strings = strings_interval), 
                         [
                             E5_4,
                          ])
        
    def test_add(self):
        C5 = position_make(strings[0], Fret.make(20, True))
        third_major = ChromaticInterval.make(4)
        self.assertEqual(C5.positions_for_interval_with_restrictions(Guitar,third_major, strings=StringDelta.SAME_STRING_ONLY(Guitar)),
                         [E5_1,])
        self.assertEqual(C5.positions_for_interval_with_restrictions(Guitar,third_major, strings=StringDelta.NEXT_STRING_ONLY(Guitar)),
                         [E5_2,])
        self.assertEqual(C5.positions_for_interval_with_restrictions(Guitar,third_major, strings=StringDelta.SAME_OR_NEXT_STRING(Guitar)),
                         [E5_1, E5_2,])
        self.assertEqual(C5.positions_for_interval_with_restrictions(Guitar,third_major, strings=StringDelta.SAME_STRING_OR_GREATER(Guitar)),
                         [E5_1, E5_2, E5_3, E5_4, E5_5, E5_6])
        self.assertEqual(C5.positions_for_interval_with_restrictions(Guitar,third_major, strings=StringDelta.NEXT_STRING_OR_GREATER(Guitar)),
                         [E5_2, E5_3, E5_4, E5_5, E5_6])
        frets = frets_make((1, 5), allow_open =True)
        expected = [E5_5, E5_6]
        actual = C5.positions_for_interval_with_restrictions(Guitar, third_major, frets=frets)
        self.assertEqual(actual, expected)
        self.assertEqual(C5.positions_for_interval_with_restrictions(Guitar,third_major, frets=frets_make((1, 5), False)),
                         [E5_5])
        
        # self.assertEqual(C5.positions_for_interval_with_restrictions(Guitar,third_major, frets=frets_make().restrict_around(C5.fret)),
        #                  [E5_1, E5_2, E5_6])
        # self.assertEqual(C5.positions_for_interval_with_restrictions(Guitar,third_major, frets=frets_make().restrict_around(C5.fret).disallow_open()),
        #                  [E5_1, E5_2])
        