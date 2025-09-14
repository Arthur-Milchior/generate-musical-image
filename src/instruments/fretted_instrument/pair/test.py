import unittest

from instruments.fretted_instrument.fretted_instrument.fretted_instruments import Guitar
from instruments.fretted_instrument.pair.generate import pairs_of_frets_values

class TestPair(unittest.TestCase):
    def test_pairs(self):
        self.assertEqual(pairs_of_frets_values(Guitar.fret(2)),
                         [
                             (0, 0), (0, 1), (0, 2),
                             (1, 0), (1, 1), (1, 2),
                             (2, 0), (2, 1)
                         ]
        )