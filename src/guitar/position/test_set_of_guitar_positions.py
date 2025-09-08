import unittest

from guitar.position.set.set_of_guitar_positions import *
from guitar.position.string.string import strings


CM_ = SetOfGuitarPositions.make([(2, 3), (3, 2), (4, 0), (5, 1)])
CM = CM_.add((6, 0))

class TestSetOfGuitarPositions(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(SetOfGuitarPositions(), SetOfGuitarPositions())
        self.assertNotEqual(SetOfGuitarPositions().add((0, 1)),
                             SetOfGuitarPositions().add((0, 2)))
        self.assertNotEqual(SetOfGuitarPositions(),
                             SetOfGuitarPositions().add((0, 2)))
        self.assertEqual(SetOfGuitarPositions().add((0, 1)),
                          SetOfGuitarPositions().add((0, 1)))
        self.assertEqual(SetOfGuitarPositions().add((0, 1)),
                          SetOfGuitarPositions().add((0, 1))
                          .add((0, 1)))
        self.assertNotEqual(SetOfGuitarPositions().add((0, 1)),
                          SetOfGuitarPositions().add((0, 1))
                          .add((0, 2)))
        
    def test_lt(self):
        self.assertLess(CM_, CM)
        self.assertLessEqual(CM_, CM)
        self.assertLessEqual(CM_, CM_)

    def test_iter(self):
        self.assertEqual(list(SetOfGuitarPositions()),
                          [])
        self.assertEqual(list(SetOfGuitarPositions().add(GuitarPosition(strings[0], Fret(1)))),
                          [GuitarPosition(strings[0], Fret(1))])
        self.assertEqual(list(SetOfGuitarPositions().add(GuitarPosition(strings[0], Fret(1)))
                               .add(GuitarPosition(strings[1], Fret(2)))),
                          [GuitarPosition(strings[0], Fret(1)), GuitarPosition(strings[1], Fret(2))])
        self.assertEqual(list(SetOfGuitarPositions().add(GuitarPosition(strings[1], Fret(2)))
                               .add(GuitarPosition(strings[0], Fret(1)))),
                          [GuitarPosition(strings[0], Fret(1)), GuitarPosition(strings[1], Fret(2))])

    def test_max_fret(self):
        self.assertEqual(SetOfGuitarPositions()._max_fret(), None)
        self.assertEqual(SetOfGuitarPositions()
                         .add(GuitarPosition(strings[0], fret=NOT_PLAYED))
                         ._max_fret(), None)
        self.assertEqual(SetOfGuitarPositions()
                         .add((0, 1))
                         ._max_fret(), Fret(1))
        self.assertEqual(SetOfGuitarPositions()
                         .add((0, 1))
                         .add((1, 2))
                         .add((3, 0))
                         ._max_fret(), Fret(2))
        
    def test_min_fret_open(self):
        self.assertEqual(SetOfGuitarPositions()._min_fret(include_open=True), None)
        self.assertEqual(SetOfGuitarPositions()
                         .add(GuitarPosition(strings[0], fret=NOT_PLAYED))
                         ._min_fret(include_open=True), None)
        self.assertEqual(SetOfGuitarPositions()
                         .add((0, 1))
                         ._min_fret(include_open=True), Fret(1))
        self.assertEqual(SetOfGuitarPositions()
                         .add((0, 0))
                         ._min_fret(include_open=True), Fret(0))
        self.assertEqual(SetOfGuitarPositions()
                         .add((0, 1))
                         .add((1, 2))
                         .add((3, 0))
                         ._min_fret(include_open=True), Fret(0))
        
    def test_min_fret_closed(self):
        self.assertEqual(SetOfGuitarPositions()._min_fret(include_open=False), None)
        self.assertEqual(SetOfGuitarPositions()
                         .add(GuitarPosition(strings[0], fret=NOT_PLAYED))
                         ._min_fret(include_open=False), None)
        self.assertEqual(SetOfGuitarPositions()
                         .add((0, 1))
                         ._min_fret(include_open=False), Fret(1))
        self.assertEqual(SetOfGuitarPositions()
                         .add((0, 0))
                         ._min_fret(include_open=False), None)
        self.assertEqual(SetOfGuitarPositions()
                         .add((0, 1))
                         .add((1, 2))
                         .add((3, 0))
                         ._min_fret(include_open=False), Fret(1))