from solfege.pattern.scale.scale_pattern import ScalePattern
from solfege.pattern_instantiation.abstract_chromatic_instantiation import AbstractChromaticInstantiation
from solfege.pattern_instantiation.scale.abstract_scale_instantiation import AbstractScale
from solfege.value.interval.chromatic_interval import ChromaticInterval
from solfege.value.interval.set.interval_list_pattern import ChromaticIntervalListPattern
from solfege.value.note.chromatic_note import ChromaticNote, ChromaticNoteFrozenList


class ChromaticScale(AbstractChromaticInstantiation[ScalePattern, int], AbstractScale[ChromaticNote, ChromaticInterval]):
    pass