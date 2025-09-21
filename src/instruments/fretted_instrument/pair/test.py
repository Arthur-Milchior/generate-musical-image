import unittest

from instruments.fretted_instrument.fretted_instrument.fretted_instruments import Guitar
from instruments.fretted_instrument.pair.generate_fretted_instrument_interval import pairs_of_frets_values
from instruments.fretted_instrument.position.fret.fret import Fret

class TestPair(unittest.TestCase):
    def test_pairs(self):
        self.assertEqual(pairs_of_frets_values(Fret.make(2, True)),
                         [
                             (0, 0), (0, 1), (0, 2),
                             (1, 0), (1, 1), (1, 2),
                             (2, 0), (2, 1)
                         ]
        )