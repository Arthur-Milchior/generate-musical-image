
from dataclasses import dataclass
from typing import ClassVar

from solfege.pattern.inversion.inversion_pattern import InversionPattern
from solfege.pattern_instantiation.inversion.abstract_inversion import AbstractInversion
from solfege.pattern_instantiation.abstract_pair_instantiation import AbstractPairInstantiation
from solfege.pattern_instantiation.inversion.chromatic_inversion import ChromaticInversion
from solfege.value.interval.abstract_interval import IntervalType
from solfege.value.interval.interval import Interval, IntervalFrozenList
from solfege.value.note.abstract_note import NoteType
from solfege.value.note.note import Note, NoteFrozenList
from utils.util import assert_typing


class Inversion(AbstractInversion[Note, Interval, NoteFrozenList, IntervalFrozenList], AbstractPairInstantiation[InversionPattern]):
    
    chromatic_instantiation_type: ClassVar = ChromaticInversion