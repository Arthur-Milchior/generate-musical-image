from dataclasses import dataclass
from typing import Iterator, List, Union
from solfege.interval.chromatic_interval import ChromaticInterval
from solfege.note.abstract_note import NoteType
from solfege.note.chromatic_note import ChromaticNote
from solfege.solfege_pattern import SolfegePattern
from solfege.interval.interval import Interval

@dataclass(frozen=True)
class IntervalPattern(SolfegePattern):
    @classmethod
    def make(cls, name: str, interval: Union[int, ChromaticInterval], *args, **kwargs):
        Interval.make_single_argument(interval)
        return super().make_relative(names=[name], relative_intervals=[interval], *args, **kwargs)


intervals_up_to_octave = [
    IntervalPattern.make("Second minor", Interval.make(diatonic=1, chromatic=1)),
    IntervalPattern.make("Second major", Interval.make(diatonic=1, chromatic=2)),
    IntervalPattern.make("Third minor", Interval.make(diatonic=2, chromatic=3)),
    IntervalPattern.make("Third major", Interval.make(diatonic=2, chromatic=4)),
    IntervalPattern.make("Fourth just", Interval.make(diatonic=3, chromatic=5)),
    IntervalPattern.make("Fourth augmented", Interval.make(diatonic=3, chromatic=6)),
    IntervalPattern.make("Fifth just", Interval.make(diatonic=5, chromatic=7)),
    IntervalPattern.make("Sixth minor", Interval.make(diatonic=5, chromatic=8)),
    IntervalPattern.make("Sixth major", Interval.make(diatonic=5, chromatic=9)),
    IntervalPattern.make("Seventh minor", Interval.make(diatonic=6, chromatic=10)),
    IntervalPattern.make("Seventh major", Interval.make(diatonic=6, chromatic=11)),
    IntervalPattern.make("Octave", Interval.make(diatonic=7, chromatic=12)),


    IntervalPattern.make("Unison augmented", Interval.make(diatonic=0, chromatic=1)),
    IntervalPattern.make("Second diminished", Interval.make(diatonic=1, chromatic=0)),
    IntervalPattern.make("Second augmented", Interval.make(diatonic=1, chromatic=3)),
    IntervalPattern.make("Third dimished", Interval.make(diatonic=2, chromatic=3)),
    IntervalPattern.make("Third augmented", Interval.make(diatonic=2, chromatic=5)),
    IntervalPattern.make("Fourth diminished", Interval.make(diatonic=3, chromatic=4)),
    IntervalPattern.make("Fifth diminished", Interval.make(diatonic=5, chromatic=6)),
    IntervalPattern.make("Fifth augmented", Interval.make(diatonic=5, chromatic=8)),
    IntervalPattern.make("Sixth diminished", Interval.make(diatonic=5, chromatic=7)),
    IntervalPattern.make("Sixth augmented", Interval.make(diatonic=5, chromatic=10)),
    IntervalPattern.make("Seventh diminished", Interval.make(diatonic=6, chromatic=9)),
    IntervalPattern.make("Seventh augmented", Interval.make(diatonic=6, chromatic=12)),
    IntervalPattern.make("Octave diminished", Interval.make(diatonic=7, chromatic=11)),
    IntervalPattern.make("Octave augmented", Interval.make(diatonic=7, chromatic=13)),
]