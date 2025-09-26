import unittest

from instruments.fretted_instrument.fretted_instrument.fretted_instruments import Guitar
from instruments.fretted_instrument.pair.generate_fretted_instrument_interval import pairs_of_frets_values
from instruments.fretted_instrument.position.fret.fret import Fret

class TestPair(unittest.TestCase):
    def test_pairs(self):
        actual = list(pairs_of_frets_values(2))
        expected = [(Fret(s, False), Fret(f,False)) for s, f in [
                             (1, 1), 
                             (1, 2), (2, 1),
                             (1, 3), (3, 1),
                         ]]
        self.assertEqual(actual,
                         expected
        )