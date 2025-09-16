
from dataclasses import dataclass
from typing import ClassVar

from solfege.pattern.inversion.identical_inversion_patterns import IdenticalInversionPatterns
from solfege.pattern_instantiation.inversion.abstract_Identical_inversions import AbstractIdenticalInversion
from solfege.pattern_instantiation.abstract_pair_instantiation import AbstractPairInstantiation
from solfege.pattern_instantiation.inversion.chromatic_identical_inversions import ChromaticIdenticalInversions
from solfege.value.interval.interval import Interval
from solfege.value.note.note import Note
from utils.util import assert_typing


class IdenticalInversion(AbstractIdenticalInversion[Note, Interval], AbstractPairInstantiation[IdenticalInversionPatterns]):
    
    chromatic_instantiation_type: ClassVar = ChromaticIdenticalInversions