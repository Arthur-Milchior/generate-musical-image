from typing import ClassVar
from lily.sheet.lily_scale_sheet import LilyScaleSheet
from lily.staff.lily_scale_staff import LilyScaleStaff
from solfege.pattern.scale.scale_pattern import ScalePattern
from solfege.pattern_instantiation.abstract_pair_instantiation import AbstractPairInstantiation
from solfege.pattern_instantiation.scale.abstract_scale_instantiation import AbstractScale
from solfege.pattern_instantiation.scale.chromatic_scale import ChromaticScale
from solfege.value.interval.interval import Interval
from solfege.value.interval.set.interval_list import IntervalList
from solfege.value.note.clef import Clef
from solfege.value.note.note import Note, NoteFrozenList




class Scale(AbstractPairInstantiation[ScalePattern, int], AbstractScale[Note, Interval]):
    """A `ScalePattern` anchored on a concrete (diatonic+chromatic) `Note` tonic -- e.g. "C melodic minor"."""

    chromatic_instantiation_type: ClassVar = ChromaticScale
    """`get_chromatic_instantiation()` builds a `ChromaticScale` from this scale."""

    def _to_lily_staff(self, clef: Clef) -> LilyScaleStaff:
        """The LilyPond staff (`LilyScaleStaff`) rendering this scale's notes on `clef`."""
        return LilyScaleStaff.make(notes = self.get_notes(), first_key = self.get_key(), clef=clef)

    def to_lily_sheet(self, clef: Clef) -> LilyScaleSheet:
        """The full LilyPond sheet (`LilyScaleSheet`) wrapping this scale's staff on `clef`."""
        return LilyScaleSheet.make(staff = self._to_lily_staff(clef))