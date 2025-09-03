import unittest

from guitar.position.set_of_guitar_positions import *
from guitar.position.string import strings

class TestSetOfGuitarPositions(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(SetOfGuitarPositions(), SetOfGuitarPositions())
        self.assertNotEqual(SetOfGuitarPositions().add(GuitarPosition(strings[0], Fret(1))),
                             SetOfGuitarPositions().add(GuitarPosition(strings[0], Fret(2))))
        self.assertNotEqual(SetOfGuitarPositions(),
                             SetOfGuitarPositions().add(GuitarPosition(strings[0], Fret(2))))
        self.assertEqual(SetOfGuitarPositions().add(GuitarPosition(strings[0], Fret(1))),
                          SetOfGuitarPositions().add(GuitarPosition(strings[0], Fret(1))))
        self.assertEqual(SetOfGuitarPositions().add(GuitarPosition(strings[0], Fret(1))),
                          SetOfGuitarPositions().add(GuitarPosition(strings[0], Fret(1)))
                          .add(GuitarPosition(strings[0], Fret(1))))
        self.assertNotEqual(SetOfGuitarPositions().add(GuitarPosition(strings[0], Fret(1))),
                          SetOfGuitarPositions().add(GuitarPosition(strings[0], Fret(1)))
                          .add(GuitarPosition(strings[0], Fret(2))))

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
        self.assertEqual(SetOfGuitarPositions()._max_fret(), NOT_PLAYED)
        self.assertEqual(SetOfGuitarPositions()
                         .add(GuitarPosition(strings[0], fret=NOT_PLAYED))
                         ._max_fret(), NOT_PLAYED)
        self.assertEqual(SetOfGuitarPositions()
                         .add(GuitarPosition(strings[0], Fret(1)))
                         ._max_fret(), Fret(1))
        self.assertEqual(SetOfGuitarPositions()
                         .add(GuitarPosition(strings[0], Fret(1)))
                         .add(GuitarPosition(strings[1], Fret(2)))
                         .add(GuitarPosition(strings[3], Fret(0)))
                         ._max_fret(), Fret(2))
        
    def test_min_fret(self):
        self.assertEqual(SetOfGuitarPositions()._min_fret(), NOT_PLAYED)
        self.assertEqual(SetOfGuitarPositions()
                         .add(GuitarPosition(strings[0], fret=NOT_PLAYED))
                         ._min_fret(), NOT_PLAYED)
        self.assertEqual(SetOfGuitarPositions()
                         .add(GuitarPosition(strings[0], Fret(1)))
                         ._min_fret(), Fret(1))
        self.assertEqual(SetOfGuitarPositions()
                         .add(GuitarPosition(strings[0], Fret(1)))
                         .add(GuitarPosition(strings[1], Fret(2)))
                         .add(GuitarPosition(strings[3], Fret(0)))
                         ._min_fret(), Fret(0))

    def test_min_non_empty_fret(self):
        self.assertEqual(SetOfGuitarPositions()._min_non_empty_fret(), NOT_PLAYED)
        self.assertEqual(SetOfGuitarPositions()
                         .add(GuitarPosition(strings[0], fret=NOT_PLAYED))
                         ._min_non_empty_fret(), NOT_PLAYED)
        self.assertEqual(SetOfGuitarPositions()
                         .add(GuitarPosition(strings[0], Fret(1)))
                         ._min_non_empty_fret(), Fret(1))
        self.assertEqual(SetOfGuitarPositions()
                         .add(GuitarPosition(strings[0], Fret(0)))
                         ._min_non_empty_fret(), NOT_PLAYED)
        self.assertEqual(SetOfGuitarPositions()
                         .add(GuitarPosition(strings[0], Fret(1)))
                         .add(GuitarPosition(strings[1], Fret(2)))
                         .add(GuitarPosition(strings[3], Fret(0)))
                         ._min_non_empty_fret(), Fret(1))
