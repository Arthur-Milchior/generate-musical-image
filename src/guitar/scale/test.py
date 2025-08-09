from solfege.solfege_pattern import SolfegePattern
from solfege.scale.scale_pattern import ScalePattern
from guitar.position.guitar_position import GuitarPosition
from .utils import scale2Pos
import unittest

majorScale = SolfegePattern.class_to_name_to_pattern[ScalePattern].get("Major")

class TestPosition(unittest.TestCase):
    def testEqual(self):
        self.assertEqual(
            scale2Pos(majorScale.get_intervals(), GuitarPosition(1, 1)),
            [GuitarPosition(1, 1), GuitarPosition(1, 3), GuitarPosition(1, 5), GuitarPosition(2, 1), GuitarPosition(2, 3),
                                                            GuitarPosition(2, 5), GuitarPosition(3, 2), GuitarPosition(3, 3)])
#print(scale2Pos(majorScale.get_intervals(), GuitarPosition(1, 2)))
