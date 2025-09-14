from typing import ClassVar
from solfege.pattern.scale.scale_pattern import ScalePattern
from solfege.pattern_instantiation.abstract_pair_instantiation import AbstractPairInstantiation
from solfege.pattern_instantiation.scale.abstract_scale_instantiation import AbstractScale
from solfege.pattern_instantiation.scale.chromatic_scale import ChromaticScale
from solfege.value.interval.interval import Interval
from solfege.value.interval.set.interval_list_pattern import IntervalListPattern
from solfege.value.note.note import Note, NoteFrozenList




class Scale(AbstractPairInstantiation[ScalePattern], AbstractScale[Note, Interval, NoteFrozenList, IntervalListPattern]):
    chromatic_instantiation_type: ClassVar = ChromaticScale