
from solfege.pattern.inversion.inversion_pattern import InversionPattern
from solfege.pattern_instantiation.abstract_chromatic_instantiation import AbstractChromaticInstantiation
from solfege.pattern_instantiation.inversion.abstract_inversion import AbstractInversion
from solfege.value.interval.interval import Interval
from solfege.value.note.note import Note


class ChromaticInversionPattern(AbstractInversion[Note, Interval], AbstractChromaticInstantiation[InversionPattern]):
    pass