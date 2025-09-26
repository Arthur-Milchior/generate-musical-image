from typing import ClassVar
from lily.sheet.lily_scale_sheet import LilyScaleSheet
from lily.staff.lily_scale_staff import LilyScaleStaff
from solfege.pattern.scale.scale_pattern import ScalePattern
from solfege.pattern_instantiation.abstract_pair_instantiation import AbstractPairInstantiation
from solfege.pattern_instantiation.scale.abstract_scale_instantiation import AbstractScale
from solfege.pattern_instantiation.scale.chromatic_scale import ChromaticScale
from solfege.value.interval.interval import Interval
from solfege.value.interval.set.interval_list_pattern import IntervalListPattern
from solfege.value.note.clef import Clef
from solfege.value.note.note import Note, NoteFrozenList




class Scale(AbstractPairInstantiation[ScalePattern, int], AbstractScale[Note, Interval]):
    chromatic_instantiation_type: ClassVar = ChromaticScale
    
    def _to_lily_staff(self, clef: Clef):
        return LilyScaleStaff.make(notes = self.get_notes(), first_key = self.get_key(), clef=clef)
    
    def to_lily_sheet(self, clef: Clef):
        return LilyScaleSheet.make(staff = self._to_lily_staff(clef))