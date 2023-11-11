from ..pos import Pos
from solfege.util import Solfege_Pattern
from solfege.scales import Scale_Pattern
from .utils import scale2Pos

majorScale = Solfege_Pattern.dic[Scale_Pattern].get("Major")

assert (scale2Pos(majorScale.get_intervals(), Pos(1, 1)) == [Pos(1, 1), Pos(1, 3), Pos(1, 5), Pos(2, 1), Pos(2, 3),
                                                            Pos(2, 5), Pos(3, 2), Pos(3, 3)])
print(scale2Pos(majorScale.get_intervals(), Pos(1, 2)))
