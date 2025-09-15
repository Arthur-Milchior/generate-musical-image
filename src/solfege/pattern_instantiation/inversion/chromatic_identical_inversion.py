
from typing import Generic
from solfege.pattern.inversion.identical_inversion_patterns import IdenticalInversionPatterns
from solfege.pattern_instantiation.abstract_chromatic_instantiation import AbstractChromaticInstantiation
from solfege.pattern_instantiation.inversion.abstract_Identical_inversions import AbstractIdenticalInversion
from solfege.value.interval.interval import Interval
from solfege.value.note.note import Note
from utils.util import T


class ChromaticIdenticalInversion(AbstractIdenticalInversion[Note, Interval], AbstractChromaticInstantiation[IdenticalInversionPatterns]):
    pass