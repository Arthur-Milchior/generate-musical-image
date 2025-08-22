import unittest

from guitar.pair.generate import pairs_of_frets_values

class TestPair(unittest.TestCase):
    def test_pairs(self):
        self.assertEqual(pairs_of_frets_values(2),
                         [
                             (0, 0), (0, 1), (0, 2),
                             (1, 0), (1, 1), (1, 2),
                             (2, 0), (2, 1)
                         ]
        )