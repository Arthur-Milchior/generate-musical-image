from dataclasses import dataclass
from typing import Tuple
import unittest

from instruments.fretted_instrument.fretted_instrument.fretted_instruments import Guitar
from instruments.fretted_instrument.position.fret.fret import Fret
from instruments.fretted_instrument.position.fretted_instrument_position import PositionOnFrettedInstrument
from instruments.fretted_instrument.position.set.set_of_fretted_instrument_positions import empty_set_of_position, SetOfPositionOnFrettedInstrument
from instruments.fretted_instrument.position.string.string import String
from instruments.fretted_instrument.chord.fretted_instrument_chord import ChordOnFrettedInstrument
from solfege.value.interval.chromatic_interval import ChromaticInterval
from solfege.value.interval.set.chromatic_interval_list_pattern import ChromaticIntervalListPattern
from utils.util import assert_typing

@dataclass(frozen=True)
class SetOfPositionOnGuitar(SetOfPositionOnFrettedInstrument):
    """Same as SetOfPositionOnFrettedInstrument, but allows to add with ints"""
    def add(self, arg):
        if isinstance(arg, tuple):
            string, fret = arg
            if isinstance(string, int):
                string = Guitar.string(string)
            if isinstance(fret, int):
                fret = Fret(fret)
            assert_typing(fret, Fret)
            assert_typing(string, String)
            arg = (string, fret)
        return super().add(arg)
    
def pos_make(string, fret):
    return PositionOnFrettedInstrument(Guitar.string(string), Fret(fret))

def _make(l):
    return SetOfPositionOnGuitar.make(positions=l)


CM_ = _make(pos_make(*pos) for pos in [(2, 3), (3, 2), (4, 0), (5, 1)])
CM = CM_.add((6, 0))

F4M = _make(pos_make(*pos) for pos in [(1, 1), (2, 3), (3, 3), (4, 2), (5, 1), (6, 1)])
G4M = _make(pos_make(*pos) for pos in [(1, 3), (2, 5), (3, 5), (4, 4), (5, 3), (6, 3)])

strings = list(Guitar.strings())

empty_set_of_fretted_instrument_position = SetOfPositionOnGuitar.make([])
not_played = Guitar.fret( value=None)

instrument = Guitar

def position_make(string, fret):
    return PositionOnFrettedInstrument(string, fret)

class TestSetOfFrettedInstrumentPositions(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(empty_set_of_fretted_instrument_position, empty_set_of_fretted_instrument_position)
        self.assertNotEqual(empty_set_of_fretted_instrument_position.add((0, 1)),
                             empty_set_of_fretted_instrument_position.add((0, 2)))
        self.assertNotEqual(empty_set_of_fretted_instrument_position,
                             empty_set_of_fretted_instrument_position.add((0, 2)))
        self.assertEqual(empty_set_of_fretted_instrument_position.add((0, 1)),
                          empty_set_of_fretted_instrument_position.add((0, 1)))
        self.assertEqual(empty_set_of_fretted_instrument_position.add((0, 1)),
                          empty_set_of_fretted_instrument_position.add((0, 1))
                          .add((0, 1)))
        self.assertNotEqual(empty_set_of_fretted_instrument_position.add((0, 1)),
                          empty_set_of_fretted_instrument_position.add((0, 1))
                          .add((0, 2)))
        
    def test_number_of_frets(self):
        self.assertEqual(CM.number_of_frets(allow_open=True), 3)
        self.assertEqual(CM.number_of_frets(allow_open=False), 2)
        
    def test_lt(self):
        self.assertLess(CM_, CM)
        self.assertLessEqual(CM_, CM)
        self.assertLessEqual(CM_, CM_)

    def test_iter(self):
        self.assertEqual(list(empty_set_of_fretted_instrument_position),
                          [])
        self.assertEqual(list(empty_set_of_fretted_instrument_position.add(position_make(strings[0], instrument.fret(1)))),
                          [position_make(strings[0], instrument.fret(1))])
        self.assertEqual(list(empty_set_of_fretted_instrument_position.add(position_make(strings[0], instrument.fret(1)))
                               .add(position_make(strings[1], instrument.fret(2)))),
                          [position_make(strings[0], instrument.fret(1)), position_make(strings[1], instrument.fret(2))])
        self.assertEqual(list(empty_set_of_fretted_instrument_position.add(position_make(strings[1], instrument.fret(2)))
                               .add(position_make(strings[0], instrument.fret(1)))),
                          [position_make(strings[0], instrument.fret(1)), position_make(strings[1], instrument.fret(2))])

    def test_max_fret(self):
        self.assertEqual(empty_set_of_fretted_instrument_position._max_fret(), None)
        self.assertEqual(empty_set_of_fretted_instrument_position
                         .add(position_make(strings[0], fret=not_played))
                         ._max_fret(), None)
        self.assertEqual(empty_set_of_fretted_instrument_position
                         .add((0, 1))
                         ._max_fret(), instrument.fret(1))
        self.assertEqual(empty_set_of_fretted_instrument_position
                         .add((0, 1))
                         .add((1, 2))
                         .add((3, 0))
                         ._max_fret(), instrument.fret(2))
        
    def test_min_fret_open(self):
        self.assertEqual(empty_set_of_fretted_instrument_position._min_fret(allow_open=True), None)
        self.assertEqual(empty_set_of_fretted_instrument_position
                         .add(position_make(strings[0], fret=not_played))
                         ._min_fret(allow_open=True), None)
        self.assertEqual(empty_set_of_fretted_instrument_position
                         .add((0, 1))
                         ._min_fret(allow_open=True), instrument.fret(1))
        self.assertEqual(empty_set_of_fretted_instrument_position
                         .add((0, 0))
                         ._min_fret(allow_open=True), instrument.fret(0))
        self.assertEqual(empty_set_of_fretted_instrument_position
                         .add((0, 1))
                         .add((1, 2))
                         .add((3, 0))
                         ._min_fret(allow_open=True), instrument.fret(0))
        
    def test_min_fret_closed(self):
        self.assertEqual(empty_set_of_fretted_instrument_position._min_fret(allow_open=False), None)
        self.assertEqual(empty_set_of_fretted_instrument_position
                         .add(position_make(strings[0], fret=not_played))
                         ._min_fret(allow_open=False), None)
        self.assertEqual(empty_set_of_fretted_instrument_position
                         .add((0, 1))
                         ._min_fret(allow_open=False), instrument.fret(1))
        self.assertEqual(empty_set_of_fretted_instrument_position
                         .add((0, 0))
                         ._min_fret(allow_open=False), None)
        self.assertEqual(empty_set_of_fretted_instrument_position
                         .add((0, 1))
                         .add((1, 2))
                         .add((3, 0))
                         ._min_fret(allow_open=False), instrument.fret(1))
        
    def test_transpose(self):
        self.assertEqual(G4M.transpose_same_string(-2, False, False), F4M)

    def test_transpose_to_fret_one(self):
        self.assertEqual(G4M.transpose_to_fret_one(), (F4M, ChromaticInterval(-2)))
        self.assertEqual(F4M.transpose_to_fret_one(), (F4M, ChromaticInterval(0)))

    def test_intervals_frow_lowest_note(self):
        frets = [0, 2, 1, 1, None, None]
        chord = ChordOnFrettedInstrument.make(instrument=Guitar, frets=frets)
        actual = chord.intervals_frow_lowest_note()
        relatives = ChromaticIntervalListPattern.make_relative([7, 4, 5])
        absolute = ChromaticIntervalListPattern.make_absolute([0, 7, 11, 16])
        self.assertEqual(actual, relatives)
        self.assertEqual(actual, absolute)
        actual = chord.intervals_frow_lowest_note_in_base_octave()
        absolute = ChromaticIntervalListPattern.make_absolute([0, 4, 7, 11])
        self.assertEqual(actual, absolute)