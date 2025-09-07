import unittest
from .guitar_position_with_finger import *

class TestGuitarPositionWithFinger(unittest.TestCase):
    def test_positions(self):
        self.assertEqual([],
                         GuitarPositionWithFinger.make(string=3, fret=6, finger=1)
                         .positions_for_interval(ChromaticInterval(1))
                         )