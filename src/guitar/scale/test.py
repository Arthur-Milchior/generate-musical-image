from ..pos import Pos
from solfege.solfege_pattern import SolfegePattern
from solfege.Scale.scale_pattern import ScalePattern
from .utils import scale2Pos

majorScale = SolfegePattern.class_to_name_to_pattern[ScalePattern].get("Major")

assert (scale2Pos(majorScale.get_intervals(), Pos(1, 1)) == [Pos(1, 1), Pos(1, 3), Pos(1, 5), Pos(2, 1), Pos(2, 3),
                                                            Pos(2, 5), Pos(3, 2), Pos(3, 3)])
print(scale2Pos(majorScale.get_intervals(), Pos(1, 2)))
