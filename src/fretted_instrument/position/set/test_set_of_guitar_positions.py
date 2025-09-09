import unittest

from fretted_instrument.position.fret.fret import NOT_PLAYED, Fret
from fretted_instrument.position.guitar_position import GuitarPosition
from fretted_instrument.position.set.set_of_guitar_positions import empty_set_of_guitar_position, SetOfGuitarPositions
from fretted_instrument.position.string.string import strings
from solfege.value.interval.chromatic_interval import ChromaticInterval


CM_ = SetOfGuitarPositions.make([(2, 3), (3, 2), (4, 0), (5, 1)])
CM = CM_.add((6, 0))

F4M = SetOfGuitarPositions.make([(1, 1), (2, 3), (3, 3), (4, 2), (5, 1), (6, 1)])
G4M = SetOfGuitarPositions.make([(1, 3), (2, 5), (3, 5), (4, 4), (5, 3), (6, 3)])

class TestSetOfGuitarPositions(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(empty_set_of_guitar_position, empty_set_of_guitar_position)
        self.assertNotEqual(empty_set_of_guitar_position.add((0, 1)),
                             empty_set_of_guitar_position.add((0, 2)))
        self.assertNotEqual(empty_set_of_guitar_position,
                             empty_set_of_guitar_position.add((0, 2)))
        self.assertEqual(empty_set_of_guitar_position.add((0, 1)),
                          empty_set_of_guitar_position.add((0, 1)))
        self.assertEqual(empty_set_of_guitar_position.add((0, 1)),
                          empty_set_of_guitar_position.add((0, 1))
                          .add((0, 1)))
        self.assertNotEqual(empty_set_of_guitar_position.add((0, 1)),
                          empty_set_of_guitar_position.add((0, 1))
                          .add((0, 2)))
        
    def test_number_of_frets(self):
        self.assertEqual(CM.number_of_frets(include_open=True), 3)
        self.assertEqual(CM.number_of_frets(include_open=False), 2)
        
    def test_lt(self):
        self.assertLess(CM_, CM)
        self.assertLessEqual(CM_, CM)
        self.assertLessEqual(CM_, CM_)

    def test_iter(self):
        self.assertEqual(list(empty_set_of_guitar_position),
                          [])
        self.assertEqual(list(empty_set_of_guitar_position.add(GuitarPosition(strings[0], Fret(1)))),
                          [GuitarPosition(strings[0], Fret(1))])
        self.assertEqual(list(empty_set_of_guitar_position.add(GuitarPosition(strings[0], Fret(1)))
                               .add(GuitarPosition(strings[1], Fret(2)))),
                          [GuitarPosition(strings[0], Fret(1)), GuitarPosition(strings[1], Fret(2))])
        self.assertEqual(list(empty_set_of_guitar_position.add(GuitarPosition(strings[1], Fret(2)))
                               .add(GuitarPosition(strings[0], Fret(1)))),
                          [GuitarPosition(strings[0], Fret(1)), GuitarPosition(strings[1], Fret(2))])

    def test_max_fret(self):
        self.assertEqual(empty_set_of_guitar_position._max_fret(), None)
        self.assertEqual(empty_set_of_guitar_position
                         .add(GuitarPosition(strings[0], fret=NOT_PLAYED))
                         ._max_fret(), None)
        self.assertEqual(empty_set_of_guitar_position
                         .add((0, 1))
                         ._max_fret(), Fret(1))
        self.assertEqual(empty_set_of_guitar_position
                         .add((0, 1))
                         .add((1, 2))
                         .add((3, 0))
                         ._max_fret(), Fret(2))
        
    def test_min_fret_open(self):
        self.assertEqual(empty_set_of_guitar_position._min_fret(include_open=True), None)
        self.assertEqual(empty_set_of_guitar_position
                         .add(GuitarPosition(strings[0], fret=NOT_PLAYED))
                         ._min_fret(include_open=True), None)
        self.assertEqual(empty_set_of_guitar_position
                         .add((0, 1))
                         ._min_fret(include_open=True), Fret(1))
        self.assertEqual(empty_set_of_guitar_position
                         .add((0, 0))
                         ._min_fret(include_open=True), Fret(0))
        self.assertEqual(empty_set_of_guitar_position
                         .add((0, 1))
                         .add((1, 2))
                         .add((3, 0))
                         ._min_fret(include_open=True), Fret(0))
        
    def test_min_fret_closed(self):
        self.assertEqual(empty_set_of_guitar_position._min_fret(include_open=False), None)
        self.assertEqual(empty_set_of_guitar_position
                         .add(GuitarPosition(strings[0], fret=NOT_PLAYED))
                         ._min_fret(include_open=False), None)
        self.assertEqual(empty_set_of_guitar_position
                         .add((0, 1))
                         ._min_fret(include_open=False), Fret(1))
        self.assertEqual(empty_set_of_guitar_position
                         .add((0, 0))
                         ._min_fret(include_open=False), None)
        self.assertEqual(empty_set_of_guitar_position
                         .add((0, 1))
                         .add((1, 2))
                         .add((3, 0))
                         ._min_fret(include_open=False), Fret(1))
        
    def test_transpose(self):
        self.assertEqual(G4M.transpose_same_string(-2, False, False), F4M)

    def test_transpose_to_fret_one(self):
        self.assertEqual(G4M.transpose_to_fret_one(), (F4M, ChromaticInterval(-2)))
        self.assertEqual(F4M.transpose_to_fret_one(), (F4M, ChromaticInterval(0)))